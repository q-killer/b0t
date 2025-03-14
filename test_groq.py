#!/usr/bin/env python3
"""test_groq.py - Core bot logic for Future Assistant v1.0"""

import os
from dotenv import load_dotenv
from groq import Groq
import sys
import subprocess
from faster_whisper import WhisperModel
import pyttsx3
import time
from trading.trading_logic import fetch_stock_data, log_trade, optimize_logic

os.environ["CT2_VERBOSE"] = "0"  # Suppress float16 warning

def load_api_key():
    """Load API keys from .env or environment variable."""
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    alpha_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not groq_key:
        print("Error: GROQ_API_KEY not found. Set it in .env or environment.")
        sys.exit(1)
    return groq_key, alpha_key

def precache_tts():
    """Precache a default TTS response."""
    for _ in range(3):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.setProperty("volume", 1.0)
            voices = engine.getProperty("voices")
            for voice in voices:
                if "female" in voice.name.lower():
                    engine.setProperty("voice", voice.id)
                    break
            engine.save_to_file("Processing your request, please wait!", "output.mp3")
            engine.runAndWait()
            print("Precached TTS to output.mp3")
            return
        except Exception as e:
            print(f"Error precaching TTS: {e}")
            time.sleep(1)
    print("Failed to precache TTS after retries")

def test_mic():
    """Test microphone by recording a short sample."""
    try:
        subprocess.run(["arecord", "-d", "1", "-f", "cd", "--quiet", "test.wav"], check=True)
        if os.path.exists("test.wav") and os.path.getsize("test.wav") > 0:
            os.remove("test.wav")
            return True
        else:
            print("Mic test failed: No audio recorded")
            return False
    except Exception as e:
        print(f"Mic test error: {e}")
        return False

def record_audio(file_path="input.wav", duration=5, retries=3):
    """Record audio using arecord with retries."""
    for attempt in range(retries):
        try:
            subprocess.run(
                ["arecord", "-d", str(duration), "-f", "cd", "--quiet", file_path],
                check=True, stderr=subprocess.PIPE
            )
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                print(f"Audio recorded to {file_path}")
                return file_path
            else:
                print(f"Attempt {attempt + 1}: No audio file created or empty")
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt + 1} error recording audio: {e.stderr.decode()}")
        time.sleep(1)
    print("Failed to record audio after retries")
    return None

def transcribe_audio(file_path):
    """Transcribe audio file to text using faster-whisper."""
    try:
        model = WhisperModel("medium.en", device="cpu")
        segments, _ = model.transcribe(file_path, beam_size=5, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))
        text = " ".join(segment.text for segment in segments)
        print(f"Transcribed: {text}")
        return text if text.strip() else None
    except Exception as e:
        print(f"Error with Whisper transcription: {e}")
        return None

def fetch_news(category="general"):
    """Fetch latest news headlines from Google News RSS."""
    for _ in range(3):
        try:
            url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
            if category == "technology":
                url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(url)
            if feed.entries:
                headlines = [entry.title for entry in feed.entries[:5]]
                return "Here are the latest headlines: " + "; ".join(headlines)
            else:
                print("No news entries found")
        except Exception as e:
            print(f"Error fetching news: {e}")
            time.sleep(1)
    return "Sorry, I couldn’t fetch the news right now!"

def extract_ticker(message):
    """Extract ticker from user input."""
    message = message.lower()
    if "nvda" in message or "nvidia" in message:
        return "NVDA"
    if "tsla" in message or "tesla" in message:
        return "TSLA"
    if "btc" in message or "bitcoin" in message:
        return "BTCUSDT"
    return None

def test_groq_message(client, message, alpha_key, model="llama3-8b-8192", max_tokens=200):
    """Send a message to Groq API and return the response."""
    main.last_message = message
    ticker = extract_ticker(message)
    for _ in range(3):
        try:
            if "news" in message.lower():
                category = "general"
                if "technology" in message.lower():
                    category = "technology"
                return fetch_news(category)
            elif ticker:
                if ticker in ["TSLA", "NVDA"]:
                    return fetch_stock_data(ticker, alpha_key)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": "You are an expert financial advisor. Provide confident, expert-level advice."}, {"role": "user", "content": message}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error contacting Groq API: {e}")
            time.sleep(1)
    print("Failed to get Groq response after retries")
    return "Sorry, I couldn’t process that right now!"

def speak_response(text):
    """Convert text to speech using pyttsx3 with female voice."""
    for _ in range(3):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.setProperty("volume", 1.0)
            voices = engine.getProperty("voices")
            for voice in voices:
                if "female" in voice.name.lower():
                    engine.setProperty("voice", voice.id)
                    break
            sentences = text.split(". ")
            for sentence in sentences:
                if sentence:
                    engine.say(sentence + ".")
                    engine.runAndWait()
                    time.sleep(0.5)
            return
        except Exception as e:
            print(f"Error with TTS: {e}")
            time.sleep(1)
    print("Failed to speak response after retries")

def main():
    """Main function to run Groq API test."""
    main.last_message = ""
    groq_key, alpha_key = load_api_key()
    client = Groq(api_key=groq_key)

    if not test_mic():
        print("Mic not working, exiting...")
        sys.exit(1)

    precache_tts()
    optimize_logic()

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

    print(f"Input: {message}")
    response = test_groq_message(client, message, alpha_key)
    print(f"Response: {response}")

    speak_response(response)

if __name__ == "__main__":
    main()
