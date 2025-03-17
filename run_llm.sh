#!/bin/bash
# Script: run_llm.sh
# Purpose: Run Qwen LLM and output Piper TTS via PipeWire/PulseAudio
# Usage: ./run_llm.sh "your prompt here" (e.g., "Analyze this: TSLA is up!")

# Check for prompt argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"<prompt>\""
    echo "Example: $0 \"Analyze this: TSLA is up!\""
    exit 1
fi
PROMPT="$1"

# Check for dependencies
for cmd in paplay sox pactl; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Error: $cmd not found. Install it: sudo apt install ${cmd/paplay/pulseaudio-utils}"
        exit 1
    fi
done

# Voice defaults
VOICE_MODEL="en_GB-vctk-medium.onnx"
SPEAKER_ID="8"  # Mia by default

# Named lady voices (VCTK speaker IDs)
case "$PROMPT" in
    *"Switch voice to Mia"*) SPEAKER_ID="8"; echo "Voice: Mia"; PROMPT="Switched to Mia";;
    *"Switch voice to Liza"*) SPEAKER_ID="42"; echo "Voice: Liza"; PROMPT="Switched to Liza";;
    *"Switch voice to Luna"*) SPEAKER_ID="45"; echo "Voice: Luna"; PROMPT="Switched to Luna";;
    *"Switch voice to Sophie"*) SPEAKER_ID="46"; echo "Voice: Sophie"; PROMPT="Switched to Sophie";;
    *"Switch voice to Ava"*) SPEAKER_ID="48"; echo "Voice: Ava"; PROMPT="Switched to Ava";;
    *"Switch voice to Tiffany"*) SPEAKER_ID="56"; echo "Voice: Tiffany"; PROMPT="Switched to Tiffany";;
    *"Switch voice to Olivia"*) SPEAKER_ID="58"; echo "Voice: Olivia"; PROMPT="Switched to Olivia";;
    *"Switch voice to Ellie"*) SPEAKER_ID="77"; echo "Voice: Ellie"; PROMPT="Switched to Ellie";;
    *"Switch voice to southern"*) VOICE_MODEL="en_GB-southern_english_female-low.onnx"; SPEAKER_ID=""; echo "Voice: Southern"; PROMPT="Switched to Southern";;
    *"Switch voice to vctk "*) 
        SPEAKER_ID=$(echo "$PROMPT" | grep -oP 'Switch voice to vctk \K\d+' || echo "8")
        if ! [[ "$SPEAKER_ID" =~ ^[0-9]+$ ]] || [ "$SPEAKER_ID" -lt 0 ] || [ "$SPEAKER_ID" -gt 108 ]; then
            echo "Invalid VCTK ID ($SPEAKER_ID)—defaulting to Mia (8)"
            SPEAKER_ID="8"
        fi
        echo "Voice: VCTK $SPEAKER_ID"; PROMPT="Switched to VCTK $SPEAKER_ID";;
esac

# Paths (relative to script location)
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
LLM_DIR="$SCRIPT_DIR/llama.cpp/build/bin"
PIPER_DIR="$SCRIPT_DIR/piper"
MODEL_PATH="$SCRIPT_DIR/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"
VOICE_MODEL_PATH="$PIPER_DIR/$VOICE_MODEL"

# Verify directories and files exist
for dir in "$LLM_DIR" "$PIPER_DIR"; do
    if [ ! -d "$dir" ]; then
        echo "Error: Directory $dir not found"
        exit 1
    fi
done
if [ ! -f "$MODEL_PATH" ]; then
    echo "Error: LLM model $MODEL_PATH not found"
    exit 1
fi
if [ ! -f "$VOICE_MODEL_PATH" ]; then
    echo "Error: Voice model $VOICE_MODEL_PATH not found"
    exit 1
fi

# Set sink
SINK="alsa_output.pci-0000_04_00.6.analog-stereo"
echo "Using sink: $SINK"

# Ensure PipeWire is ready and sink is running
systemctl --user restart pipewire pipewire-pulse
echo "Restarting PipeWire..."
sleep 5  # Wait for services
if ! pactl list sinks | grep -q "$SINK"; then
    echo "Error: Sink $SINK not found. Available sinks:"
    pactl list sinks short
    exit 1
fi
pactl set-sink-mute "$SINK" 0
pactl set-sink-volume "$SINK" 75%
pactl set-default-sink "$SINK"
pactl suspend-sink "$SINK" 0

# Force sink to RUNNING state
echo "Waking sink..."
until pactl list sinks | grep -A1 "$SINK" | grep -q "State: RUNNING"; do
    paplay --device="$SINK" /dev/zero -t raw -r 48000 -c 2 -f s32le -d 1 2>/dev/null
    sleep 1
    echo "Waiting for sink to activate..."
done
echo "Sink activated:"
pactl list sinks | grep -E "Name|State" > sink_wake.log
cat sink_wake.log

# Run LLM analysis
cd "$LLM_DIR" || exit 1
OUTPUT=$(./llama-cli -m "$MODEL_PATH" -p "$PROMPT" -n 128 --no-conversation 2>/dev/null)
if [ -z "$OUTPUT" ]; then
    echo "Error: LLM output is empty"
    exit 1
fi
echo "LLM Output: $OUTPUT"

# Generate voice output with Piper
cd "$PIPER_DIR" || exit 1
rm -f output.wav output_converted.wav
PIPER_CMD="./piper --model \"$VOICE_MODEL_PATH\""
[ -n "$SPEAKER_ID" ] && PIPER_CMD="$PIPER_CMD --speaker \"$SPEAKER_ID\""
PIPER_CMD="$PIPER_CMD --output_file \"$PIPER_DIR/output.wav\" 2>error.log"

LD_LIBRARY_PATH=$PWD bash -c "echo \"\$OUTPUT\" | $PIPER_CMD"
if [ ! -f "$PIPER_DIR/output.wav" ]; then
    echo "Error: Piper failed to generate output.wav—check error.log"
    cat error.log
    exit 1
fi
WAV_SIZE=$(stat -c%s "$PIPER_DIR/output.wav")
if [ "$WAV_SIZE" -lt 100 ]; then
    echo "Error: output.wav is too small ($WAV_SIZE bytes)—likely empty"
    cat error.log
    exit 1
fi

# Convert to PipeWire-compatible format
sox "$PIPER_DIR/output.wav" -r 48000 -c 2 -e signed-integer -b 32 "$PIPER_DIR/output_converted.wav" 2>sox.log
if [ ! -f "$PIPER_DIR/output_converted.wav" ]; then
    echo "Error: sox conversion failed—check sox.log"
    cat sox.log
    exit 1
fi

# Play audio with paplay
echo "Playing: $PIPER_DIR/output_converted.wav"
pactl list sinks short > sink_state_before.log
paplay --device="$SINK" --verbose "$PIPER_DIR/output_converted.wav" 2>playback.log
PLAYBACK_STATUS=$?
pactl list sinks short > sink_state_after.log
if [ $PLAYBACK_STATUS -ne 0 ]; then
    echo "Error: paplay failed (status $PLAYBACK_STATUS)"
    cat playback.log
else
    echo "Playback completed"
    cat playback.log
fi
echo "Sink state before:"; cat sink_state_before.log
echo "Sink state after:"; cat sink_state_after.log
rm -f "$PIPER_DIR/output.wav" "$PIPER_DIR/output_converted.wav" playback.log sink_state_before.log sink_state_after.log sox.log sink_wake.log
