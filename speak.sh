#!/bin/bash
# Script: speak.sh
# Purpose: Handle voice output with Piper TTS, including named lady voices
# Usage: ./speak.sh "text to speak" "original prompt" (prompt checks for voice switch)

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 \"text to speak\" \"original prompt\""
    exit 1
fi
TEXT="$1"
PROMPT="$2"

# Voice defaults
VOICE_MODEL="en_GB-vctk-medium.onnx"
SPEAKER_ID="8"  # Mia by default

# Named lady voices (VCTK speaker IDs)
# Mia=8, Liza=42, Luna=45, Sophie=46, Ava=48, Tiffany=56, Olivia=58, Ellie=77
case "$PROMPT" in
    *"Switch voice to Mia"*) SPEAKER_ID="8"; echo "Voice: Mia";;
    *"Switch voice to Liza"*) SPEAKER_ID="42"; echo "Voice: Liza";;
    *"Switch voice to Luna"*) SPEAKER_ID="45"; echo "Voice: Luna";;
    *"Switch voice to Sophie"*) SPEAKER_ID="46"; echo "Voice: Sophie";;
    *"Switch voice to Ava"*) SPEAKER_ID="48"; echo "Voice: Ava";;
    *"Switch voice to Tiffany"*) SPEAKER_ID="56"; echo "Voice: Tiffany";;
    *"Switch voice to Olivia"*) SPEAKER_ID="58"; echo "Voice: Olivia";;
    *"Switch voice to Ellie"*) SPEAKER_ID="77"; echo "Voice: Ellie";;
    *"Switch voice to southern"*) VOICE_MODEL="en_GB-southern_english_female-low.onnx"; SPEAKER_ID=""; echo "Voice: Southern";;
    *"Switch voice to vctk "*) 
        SPEAKER_ID=$(echo "$PROMPT" | grep -oP 'Switch voice to vctk \K\d+' || echo "8")
        if ! [[ "$SPEAKER_ID" =~ ^[0-9]+$ ]] || [ "$SPEAKER_ID" -lt 0 ] || [ "$SPEAKER_ID" -gt 108 ]; then
            echo "Invalid VCTK ID ($SPEAKER_ID)—defaulting to Mia (8)"
            SPEAKER_ID="8"
        fi
        echo "Voice: VCTK $SPEAKER_ID";;
esac

# Paths
PIPER_DIR="$HOME/bot/piper"
[ ! -d "$PIPER_DIR" ] && { echo "Error: $PIPER_DIR not found"; exit 1; }
[ ! -f "$PIPER_DIR/$VOICE_MODEL" ] && { echo "Error: $PIPER_DIR/$VOICE_MODEL not found"; exit 1; }

# Generate voice
cd "$PIPER_DIR" || { echo "Failed to cd to $PIPER_DIR"; exit 1; }
rm -f output.wav
PIPER_CMD="./piper --model \"$VOICE_MODEL\""
[ -n "$SPEAKER_ID" ] && PIPER_CMD="$PIPER_CMD --speaker \"$SPEAKER_ID\""
PIPER_CMD="$PIPER_CMD --output_file output.wav 2>error.log"

LD_LIBRARY_PATH=$PWD bash -c "echo \"\$TEXT\" | $PIPER_CMD"
[ ! -f "output.wav" ] && { echo "Error: Piper failed—check error.log"; cat error.log; exit 1; }

# Play with timeout
timeout 30s aplay output.wav 2>/dev/null || echo "Warning: aplay failed or timed out"
rm -f output.wav
