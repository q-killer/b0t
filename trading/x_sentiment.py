import tweepy
from datetime import datetime
import re

# X API credentials - REPLACE with your own!
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with X
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def scan_x_tickers(tickers=["TSLA", "AAPL"], max_tweets=100):
    """Scan X for ticker mentions and basic sentiment."""
    results = {}
    for ticker in tickers:
        query = f"${ticker} -filter:retweets"
        tweets = api.search_tweets(q=query, count=max_tweets, lang="en")
        volume = len(tweets)
        sentiment_score = 0
        for tweet in tweets:
            text = tweet.text.lower()
            if "bull" in text or "up" in text or "buy" in text:
                sentiment_score += 1
            elif "bear" in text or "down" in text or "sell" in text:
                sentiment_score -= 1
        results[ticker] = {"volume": volume, "sentiment": sentiment_score}
    return results

def main():
    tickers = ["TSLA", "AAPL", "NVDA"]
    print(f"[{datetime.now()}] Scanning X for {tickers}...")
    
    # Fetch X data
    trends = scan_x_tickers(tickers)
    
    # Display results
    print("\nX Sentiment & Volume Report:")
    for ticker, data in trends.items():
        sentiment = "Positive" if data["sentiment"] > 0 else "Negative" if data["sentiment"] < 0 else "Neutral"
        print(f"{ticker} | Volume: {data['volume']} | Sentiment: {sentiment} (Score: {data['sentiment']})")

if __name__ == "__main__":
    main()
