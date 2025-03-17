#!/bin/bash

# Voice model selection
# - en_GB-southern_english_female-low.onnx: Sultry, low British female (no speaker ID)
# - en_GB-vctk-medium.onnx: Multi-voice pack, 109 speakers (0-108), use --speaker N
# To change voice, say: "Switch voice to southern" or "Switch voice to vctk N" (N = 0-108)
VOICE_MODEL="en_GB-vctk-medium.onnx"  # Default to VCTK
SPEAKER_ID="8"  # Default to speaker 8—sultry pick

# Check for voice switch command in prompt
PROMPT="Analyze this: The market is bullish today!"
if [[ "$PROMPT" =~ "Switch voice to southern" ]]; then
    VOICE_MODEL="en_GB-southern_english_female-low.onnx"
    SPEAKER_ID=""
elif [[ "$PROMPT" =~ "Switch voice to vctk" ]]; then
    VOICE_MODEL="en_GB-vctk-medium.onnx"
    SPEAKER_ID=$(echo "$PROMPT" | grep -oP 'Switch voice to vctk \K\d+' || echo "8")  # Default 8
fi

cd ~/bot/llama.cpp/build/bin
OUTPUT=$(./llama-cli -m ~/bot/models/qwen2.5-0.5b-instruct-q4_k_m.gguf -p "$PROMPT" -n 128 --no-conversation 2>/dev/null)
if [ -z "$OUTPUT" ]; then
    echo "Error: LLM output is empty"
    exit 1
fi
echo "$OUTPUT"

cd ~/bot/piper
rm -f output.wav  # Clear old WAV to avoid lock
if [ -n "$SPEAKER_ID" ]; then
    LD_LIBRARY_PATH=$PWD ./piper --model "$VOICE_MODEL" --speaker "$SPEAKER_ID" --output_file output.wav 2>error.log <<EOL
$OUTPUT
EOL
else
    LD_LIBRARY_PATH=$PWD ./piper --model "$VOICE_MODEL" --output_file output.wav 2>error.log <<EOL
$OUTPUT
EOL
fi

if [ -f "output.wav" ]; then
    aplay output.wav
    rm output.wav
else
    echo "Error: Piper failed—check error.log"
    cat error.log
fi
