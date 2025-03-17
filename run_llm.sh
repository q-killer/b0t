#!/bin/bash
# Script: run_llm.sh
# Purpose: Run Qwen LLM to analyze prompts and trigger voice output via speak.sh
# Usage: ./run_llm.sh "your prompt here" (e.g., "Analyze this: TSLA is up!")

# Check for prompt argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"<prompt>\""
    echo "Example: $0 \"Analyze this: The market is bullish today!\""
    exit 1
fi
PROMPT="$1"

# Paths
LLM_DIR="$HOME/bot/llama.cpp/build/bin"
MODEL_PATH="$HOME/bot/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"

# Verify paths
[ ! -d "$LLM_DIR" ] && { echo "Error: $LLM_DIR not found"; exit 1; }
[ ! -f "$MODEL_PATH" ] && { echo "Error: $MODEL_PATH not found"; exit 1; }

# Run LLM analysis
cd "$LLM_DIR" || { echo "Failed to cd to $LLM_DIR"; exit 1; }
OUTPUT=$(./llama-cli -m "$MODEL_PATH" -p "$PROMPT" -n 128 --no-conversation 2>/dev/null)
[ -z "$OUTPUT" ] && { echo "Error: LLM output is empty"; exit 1; }

# Pass output to speak.sh
bash "$HOME/bot/speak.sh" "$OUTPUT" "$PROMPT"
