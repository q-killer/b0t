#!/usr/bin/env python3
"""test_groq.py - Core bot logic for Future Assistant v1.0 with yfinance"""

import os
os.environ["CT2_VERBOSE"] = "0"
import sys
import subprocess
import time
import yfinance as yf
from dotenv import load_dotenv
from groq import Groq
from faster_whisper import WhisperModel

def log_debug(message):
    print(f"[DEBUG {time.strftime('%H:%M:%S')}]: {message}", flush=True)

def load_api_key():
    log_debug("Loading API keys")
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        log_debug("Error: GROQ_API_KEY not found")
        sys.exit(1)
    return groq_key

def get_stock_data(ticker):
    log_debug(f"Fetching yfinance data for {ticker}")
    try:
        stock = yf.Ticker(ticker)
        today = stock.history(period="1d")
        month = stock.history(period="1mo")
        if today.empty or month.empty:
            return f"No data available for {ticker}"
        current = today["Close"].iloc[-1]
        high = month["High"].max()
        low = month["Low"].min()
        return f"{ticker} on {time.strftime('%Y-%m-%d')}: Current ${current:.2f}, 1-month range ${low:.2f}–${high:.2f}"
    except Exception as e:
        log_debug(f"yfinance error: {e}")
        return f"Couldn’t fetch data for {ticker}"

def speak_response(text):
    log_debug(f"TTS Speaking: {text}")
    try:
        subprocess.run(["pkill", "-f", "festival"], check=False)
        with open("tts_temp.txt", "w") as f:
            f.write("(voice_cmu_us_slt_arctic_hts)\n")
            sentences = text.split(". ")
            for sentence in sentences:
                if sentence:
                    safe_sentence = sentence.replace('"', '\\"').replace('(', '\\(').replace(')', '\\)')
                    f.write(f'(SayText "{safe_sentence}.")\n')
        process = subprocess.Popen(["festival", "--pipe"], stdin=open("tts_temp.txt"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=40)
        os.remove("tts_temp.txt")
        if process.returncode != 0:
            log_debug(f"TTS Failed: {stderr.decode()}")
        else:
            log_debug("TTS Success")
    except subprocess.TimeoutExpired:
        log_debug("TTS Timeout, killing process")
        process.kill()
        subprocess.run(["pkill", "-f", "festival"], check=False)
    except Exception as e:
        log_debug(f"TTS Error: {e}")

def record_audio(file_path="input.wav", duration=5):
    log_debug("Recording audio")
    try:
        process = subprocess.Popen(
            ["arecord", "-d", str(duration), "-f", "cd", "--quiet", "-r", "44100", file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(timeout=duration + 2)
        if process.returncode != 0 or not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            log_debug(f"Recording failed: {stderr.decode()}")
            return None
        log_debug(f"Audio recorded to {file_path}")
        return file_path
    except subprocess.TimeoutExpired:
        log_debug("Recording timeout, killing process")
        process.kill()
        return None
    except Exception as e:
        log_debug(f"Recording error: {e}")
        return None

def transcribe_audio(file_path):
    log_debug("Transcribing audio")
    try:
        model = WhisperModel("medium.en", device="cpu")
        segments, _ = model.transcribe(file_path, beam_size=5, vad_filter=True)
        text = " ".join(segment.text for segment in segments)
        log_debug(f"Transcribed: {text}")
        return text if text.strip() else None
    except Exception as e:
        log_debug(f"Transcription error: {e}")
        return None

def test_groq_message(client, message):
    log_debug(f"Sending to Groq: {message}")
    try:
        # Check for stock-related queries
        stock_data = ""
        if "stock" in message.lower():
            tickers = ["NVDA", "SPY"]  # Add more as needed
            for ticker in tickers:
                if ticker.lower() in message.lower() or "market" in message.lower():
                    stock_data += get_stock_data(ticker) + "\n"
        prompt = f"It is March 14, 2025. You are an expert financial advisor and profitable investor, skilled in stocks, crypto, futures, and currencies. Use this data:\n{stock_data}Provide specific, confident recommendations based on market data and trends as of March 14, 2025, no disclaimers or hedging."
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=50
        )
        return response.choices[0].message.content
    except Exception as e:
        log_debug(f"Groq error: {e}")
        return "Sorry, I couldn’t process that right now!"

def main():
    log_debug("Starting main")
    groq_key = load_api_key()
    client = Groq(api_key=groq_key)

    log_debug("Recording 5 seconds of audio")
    audio_file = record_audio()
    if not audio_file:
        message = "Say hi in 10 words or less"
        log_debug(f"No audio, using default: {message}")
    else:
        message = transcribe_audio(audio_file)
        if not message:
            message = "Say hi in 10 words or less"
            log_debug(f"No transcription, using default: {message}")

    log_debug(f"Input: {message}")
    response = test_groq_message(client, message)
    log_debug(f"Response: {response}")
    speak_response(response)

if __name__ == "__main__":
    main()
import pyttsx3

# Display colorful welcome with ASCII art
print('\033[1;34m  ____        _        \033[0m')
print('\033[1;34m / ___| _ __ | |_ _   _ \033[0m')
print('\033[1;34m \___ \| '_ \| __| | | |\033[0m')
print('\033[1;34m  ___) | | | | |_| |_| |\033[0m')
print('\033[1;34m |____/|_| |_|___|\__, |\033[0m')
print('\033[1;34m                  |___/ \033[0m')
print('\033[1;32mYo, what’s next? Pick an option (1-3):\033[0m')
print('1. Ask a question')
print('2. Check stock data')
print('3. Exit')

# Placeholder for main logic
engine = pyttsx3.init()
engine.runAndWait()
