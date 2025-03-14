#!/bin/bash
# Test the Future Assistant with Whisper and TTS
cd ~/bot || { echo "Error: ~/bot directory not found"; exit 1; }
source ~/bot/myenv/bin/activate
./test_groq.py || { echo "Error running test_groq.py"; exit 1; }
