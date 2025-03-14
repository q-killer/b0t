#!/usr/bin/env python3
"""test_groq.py - Robust Groq API test with trading logic for Future Assistant v1.0"""

import os
from dotenv import load_dotenv
from groq import Groq
import sys
import subprocess
from faster_whisper import WhisperModel
import pyttsx3
import feedparser
import time
import yfinance as yf
import requests
from datetime import datetime, timedelta

def load_api_key():
    """Load the Groq API key from .env or environment variable."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found. Set it in .env or environment.")
        sys.exit(1)
    return api_key

def precache_tts():
    """Precache a default TTS response."""
    for _ in range(3):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.setProperty("volume", 1.0)
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

def fetch_stock_data(ticker="TSLA"):
    """Fetch stock data and basic sentiment."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d", interval="1d")
        if hist.empty:
            return f"No data for {ticker}"
        latest = hist.iloc[-1]
        prev = hist.iloc[-2]
        change = ((latest["Close"] - prev["Close"]) / prev["Close"]) * 100
        volume = latest["Volume"]
        rsi = calc_rsi(hist["Close"].values)  # Simple 14-day RSI
        advice = trading_logic(ticker, change, volume, rsi)
        return f"{ticker} latest: ${latest['Close']:.2f}, Change: {change:.2f}%, Volume: {volume:,}, RSI: {rsi:.2f}. {advice}"
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return f"Couldn’t fetch {ticker} data!"

def fetch_crypto_data(symbol="BTCUSDT"):
    """Fetch crypto data from Binance."""
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        resp = requests.get(url).json()
        price = float(resp["lastPrice"])
        change = float(resp["priceChangePercent"])
        volume = float(resp["volume"])
        advice = trading_logic(symbol, change, volume, None)  # No RSI for simplicity
        return f"{symbol} latest: ${price:.2f}, Change: {change:.2f}%, Volume: {volume:,.2f}. {advice}"
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        return f"Couldn’t fetch {symbol} data!"

def calc_rsi(prices, period=14):
    """Calculate RSI for stock data."""
    if len(prices) < period + 1:
        return 50.0  # Neutral default
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    return 100 - (100 / (1 + rs))

def trading_logic(ticker, change, volume, rsi=None):
    """Ross Cameron-inspired momentum logic with risk management."""
    sentiment = "neutral"
    if "news" in main.last_message.lower():  # Tie to last user input
        sentiment = "positive" if change > 1 else "negative" if change < -1 else "neutral"
    
    if rsi and rsi > 70:
        return f"Overbought - consider selling {ticker} with a tight stop."
    elif rsi and rsi < 30:
        return f"Oversold - consider buying {ticker} with a tight stop."
    
    if volume > 1_000_000 and change > 2:  # Momentum breakout
        return f"Buy {ticker} on breakout, set stop at 1% below entry, target 3% profit."
    elif change < -2 and sentiment != "positive":
        return f"Sell {ticker} short, set stop at 1% above entry, target 2% profit."
    return f"Hold {ticker} - no clear signal yet."

def test_groq_message(client, message, model="llama3-8b-8192", max_tokens=200):
    """Send a message to Groq API and return the response, with trading logic."""
    main.last_message = message  # Store for sentiment tie-in
    for _ in range(3):
        try:
            if "news" in message.lower():
                category = "general"
                if "technology" in message.lower():
                    category = "technology"
                return fetch_news(category)
            elif "stock" in message.lower() or "tsla" in message.lower():
                return fetch_stock_data("TSLA")  # Default to TSLA for now
            elif "crypto" in message.lower() or "btc" in message.lower():
                return fetch_crypto_data("BTCUSDT")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error contacting Groq API: {e}")
            time.sleep(1)
    print("Failed to get Groq response after retries")
    return "Sorry, I couldn’t process that right now!"

def speak_response(text):
    """Convert text to speech using pyttsx3."""
    for _ in range(3):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()
            return
        except Exception as e:
            print(f"Error with TTS: {e}")
            time.sleep(1)
    print("Failed to speak response after retries")

def main():
    """Main function to run Groq API test with trading logic."""
    main.last_message = ""  # Initialize last_message
    api_key = load_api_key()
    client = Groq(api_key=api_key)

    if not test_mic():
        print("Mic not working, exiting...")
        sys.exit(1)

    precache_tts()

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
    response = test_groq_message(client, message)
    print(f"Response: {response}")

    speak_response(response)

if __name__ == "__main__":
    main()
