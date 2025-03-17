#!/usr/bin/env python3
# Script: voice_input.py
# Purpose: Listen for "Hey b0t" and pass commands to run_llm.sh, persist voice state

import speech_recognition as sr
import subprocess
import os
import time

# Persistent voice state
VOICE_FILE = os.path.expanduser("~/bot/voice_state.txt")
if os.path.exists(VOICE_FILE):
    with open(VOICE_FILE, "r") as f:
        CURRENT_VOICE = f.read().strip()
else:
    CURRENT_VOICE = "Mia"

def save_voice(voice):
    global CURRENT_VOICE
    CURRENT_VOICE = voice
    with open(VOICE_FILE, "w") as f:
        f.write(voice)

def call_llm(prompt):
    result = subprocess.run(['bash', os.path.expanduser('~/bot/run_llm.sh'), prompt], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"LLM error: {result.stderr}")
    output = result.stdout.strip()
    # Persist voice if switched
    for voice in ["Mia", "Liza", "Luna", "Sophie", "Ava", "Tiffany", "Olivia", "Ellie", "southern"]:
        if f"Switch voice to {voice}" in prompt:
            save_voice(voice)
            break
    return output

def callback(recognizer, audio):
    try:
        command = recognizer.recognize_google(audio)
        print(f"Heard: {command}")
        if command.lower().startswith("hey bot"):
            prompt = command[7:].strip()
            print(f"Processing: {prompt}")
            call_llm(prompt)
    except sr.UnknownValueError:
        print("Couldn’t understand audio—check mic or speak clearer")
    except sr.RequestError as e:
        print(f"Google API error: {e}—check internet")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Initialize recognizer and mic
recognizer = sr.Recognizer()
mic = sr.Microphone()
print("Available microphones:")
for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {mic_name}")

with mic as source:
    print("Adjusting for ambient noise (2 seconds)...")
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print(f"Listening for 'Hey b0t' with voice: {CURRENT_VOICE}...")

stop_listening = recognizer.listen_in_background(mic, callback)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping...")
    stop_listening(wait_for_stop=False)
