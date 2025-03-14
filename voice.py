#!/usr/bin/env python3
"""voice.py - Voice input test for Future Assistant v1.0"""

import speech_recognition as sr
import sys

def get_voice_input(device_index=3):
    """Capture voice input from the microphone."""
    r = sr.Recognizer()
    try:
        with sr.Microphone(device_index=device_index) as source:
            print("Say something!")
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
    except sr.UnknownValueError:
        print("Sorry, I couldn’t understand that.")
        return None
    except sr.RequestError as e:
        print(f"Error with recognition service: {e}")
        return None
    except Exception as e:
        print(f"Microphone error: {e}")
        return None

if __name__ == "__main__":
    text = get_voice_input()
    if text:
        print(f"Voice input captured: {text}")
    else:
        sys.exit(1)
