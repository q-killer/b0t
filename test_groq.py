#!/usr/bin/env python3
"""test_groq.py - Groq API test with Whisper audio input and TTS for Future Assistant v1.0"""

import os
from dotenv import load_dotenv
from groq import Groq
import sys
import subprocess
from faster_whisper import WhisperModel
from gtts import gTTS
import pygame.mixer

def load_api_key():
    """Load the Groq API key from .env or environment variable."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found. Set it in .env or environment.")
        sys.exit(1)
    return api_key

def record_audio(file_path="input.wav", duration=5):
    """Record audio using arecord and return the file path."""
    try:
        subprocess.run(
            ["arecord", "-d", str(duration), "-f", "cd", "--quiet", file_path],
            check=True, stderr=subprocess.PIPE
        )
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"Audio recorded to {file_path}")
            return file_path
        else:
            print("Error: No audio file created or empty")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error recording audio: {e.stderr.decode()}")
        return None

def transcribe_audio(file_path):
    """Transcribe audio file to text using faster-whisper."""
    try:
        model = WhisperModel("medium.en", device="cpu")
        segments, _ = model.transcribe(file_path, beam_size=5, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))  # Less strict VAD
        text = " ".join(segment.text for segment in segments)
        print(f"Transcribed: {text}")
        return text if text.strip() else None
    except Exception as e:
        print(f"Error with Whisper transcription: {e}")
        return None

def test_groq_message(client, message, model="llama3-8b-8192", max_tokens=200):
    """Send a message to Groq API and return the response."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error contacting Groq API: {e}")
        sys.exit(1)

def speak_response(text, file_path="output.mp3"):
    """Convert text to speech using gTTS and play with pygame."""
    try:
        tts = gTTS(text=text, lang="en")
        tts.save(file_path)
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error with TTS: {e}")

def main():
    """Main function to run Groq API test with Whisper audio input and TTS."""
    api_key = load_api_key()
    client = Groq(api_key=api_key)

    # Record and transcribe audio
    print("Recording 5 seconds of audio...")
    audio_file = record_audio()
    if not audio_file:
        message = "Say hi in 10 words or less"
        print(f"No audio recorded, using default: {message}")
    else:
        message = transcribe_audio(audio_file)
        if not message:
            message = "Say hi in 10 words or less"
            print(f"No transcription, using default: {message}")

    # Send to Groq and get response
    print(f"Input: {message}")
    response = test_groq_message(client, message)
    print(f"Response: {response}")

    # Speak the response
    speak_response(response)

if __name__ == "__main__":
    main()
