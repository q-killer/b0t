import requests
import json
from datetime import datetime

# Alpha Vantage API key - Isaac's key
API_KEY = "J98G60L2CTH4X84K"
BASE_URL = "https://www.alphavantage.co/query"

def fetch_news(tickers=["TSLA", "AAPL"], limit=10):
    """Fetch financial news for tickers from Alpha Vantage."""
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ",".join(tickers),
        "apikey": API_KEY,
        "limit": limit
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if "feed" not in data:
            print("No news feed found - check API key or ticker list.")
            return []
        return data["feed"]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def analyze_sentiment(news_feed):
    """Basic sentiment analysis - positive/negative mentions."""
    sentiment_scores = []
    for article in news_feed:
        ticker_sentiment = article.get("ticker_sentiment", [])
        for ts in ticker_sentiment:
            score = float(ts["ticker_sentiment_score"])
            sentiment_scores.append({
                "ticker": ts["ticker"],
                "score": score,
                "title": article["title"],
                "time": article["time_published"]
            })
    return sentiment_scores

def main():
    # Configurable ticker list
    tickers = ["TSLA", "AAPL", "NVDA"]
    print(f"[{datetime.now()}] Scanning news for {tickers}...")
    
    # Fetch and analyze news
    news_feed = fetch_news(tickers, limit=10)
    if not news_feed:
        return
    
    sentiment_scores = analyze_sentiment(news_feed)
    
    # Display results
    print("\nNews Sentiment Report:")
    for item in sentiment_scores:
        sentiment = "Positive" if item["score"] > 0 else "Negative" if item["score"] < 0 else "Neutral"
        print(f"{item['ticker']} | {sentiment} (Score: {item['score']:.2f}) | "
              f"{item['title']} | {item['time']}")

if __name__ == "__main__":
    main()
