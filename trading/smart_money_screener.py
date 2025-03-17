#!/usr/bin/env python3
# Smart money screener: options, futures, expirations, and obscure signals

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Alpha Vantage API key (Isaac's)
ALPHA_KEY = "J98G60L2CTH4X84K"
ALPHA_BASE = "https://www.alphavantage.co/query"

# Finviz URL (replace with API if you get a key)
FINVIZ_URL = "https://finviz.com/screener.ashx"

def fetch_finviz_options_flow(filters={"optionable": "Yes", "market_cap": "+Small"}):
    """Scrape Finviz for stocks with high options activity (API preferred if key added)."""
    params = {
        "v": 111,  # Screener view
        "f": "cap_smallover,sh_opt_option",  # Small-cap, optionable
        "r": 0  # Results page
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(FINVIZ_URL, params=params, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "screener-body-table"})
        if not table:
            return []
        rows = table.find_all("tr")[1:11]  # Top 10 results
        tickers = [row.find_all("td")[1].text for row in rows]
        return tickers
    except Exception as e:
        print(f"Finviz scrape failed: {e}")
        return []

def fetch_alpha_futures(symbol):
    """Get futures data from Alpha Vantage (proxy for smart money moves)."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": f"{symbol}=F",  # Futures notation (e.g., CL=F for crude oil)
        "apikey": ALPHA_KEY
    }
    try:
        response = requests.get(ALPHA_BASE, params=params)
        data = response.json()
        if "Time Series (Daily)" not in data:
            return None
        df = pd.DataFrame(data["Time Series (Daily)"]).T
        df["4. close"] = df["4. close"].astype(float)
        return df["4. close"].iloc[0]  # Latest close
    except Exception as e:
        print(f"Alpha futures fetch failed for {symbol}: {e}")
        return None

def options_expiration_signal(ticker):
    """Estimate options expiration impact (simplified - expand with real data)."""
    # Placeholder: Real API (e.g., CBOE) would give open interest/volume
    today = datetime.now()
    third_friday = today + timedelta(days=(18 - today.weekday() + 7) % 7)  # Rough 3rd Fri
    days_to_expiry = (third_friday - today).days
    return days_to_expiry < 5  # High impact if near expiry

def web_x_signal(ticker):
    """Quick web/X scan for unusual activity (placeholder - expand with Tweepy)."""
    # Simplified: Real impl. would use X API or web crawl
    return np.random.choice([True, False])  # Mock signal

def screen_stocks():
    """Main screener: Combine smart money signals for profitable opportunities."""
    print(f"[{datetime.now()}] Running Smart Money Screener...")
    
    # Step 1: Get optionable stocks from Finviz
    candidates = fetch_finviz_options_flow()
    if not candidates:
        print("No candidates found.")
        return
    
    # Step 2: Analyze each candidate
    results = []
    for ticker in candidates[:5]:  # Limit to 5 for speed
        # Futures proxy (e.g., correlate stock to sector futures)
        futures_price = fetch_alpha_futures(ticker[:2])  # Rough sector match
        futures_signal = futures_price > 0 if futures_price else False
        
        # Options expiration
        expiry_signal = options_expiration_signal(ticker)
        
        # Web/X chatter
        chatter_signal = web_x_signal(ticker)
        
        # Score: Weight signals (tweak as needed)
        score = sum([futures_signal, expiry_signal, chatter_signal]) / 3
        if score > 0.5:  # Threshold for "opportunity"
            results.append({
                "ticker": ticker,
                "score": score,
                "futures": futures_price or "N/A",
                "near_expiry": expiry_signal,
                "chatter": chatter_signal
            })
    
    # Step 3: Display results
    print("\nSmart Money Opportunities:")
    for r in results:
        print(f"{r['ticker']} | Score: {r['score']:.2f} | "
              f"Futures: {r['futures']} | Near Expiry: {r['near_expiry']} | "
              f"Chatter: {r['chatter']}")

if __name__ == "__main__":
    screen_stocks()
