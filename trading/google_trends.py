from pytrends.request import TrendReq
from datetime import datetime

# Initialize pytrends
pytrends = TrendReq(hl="en-US", tz=360)

def check_trends(tickers=["TSLA", "AAPL"]):
    """Check Google Trends for ticker search interest spikes."""
    results = {}
    for ticker in tickers:
        pytrends.build_payload([ticker], timeframe="now 7-d", geo="US")
        data = pytrends.interest_over_time()
        if ticker in data and not data.empty:
            recent = data[ticker][-24:]  # Last 24 hours
            avg = recent.mean()
            spike = recent.max() > avg * 1.5  # 50% above avg = spike
            results[ticker] = {"interest": int(recent.max()), "spike": spike}
    return results

def main():
    tickers = ["TSLA", "AAPL", "NVDA"]
    print(f"[{datetime.now()}] Scanning Google Trends for {tickers}...")
    
    # Fetch trends
    trends = check_trends(tickers)
    
    # Display results
    print("\nGoogle Trends Report:")
    for ticker, data in trends.items():
        spike_text = "Yes" if data["spike"] else "No"
        print(f"{ticker} | Peak Interest: {data['interest']} | Spike? {spike_text}")

if __name__ == "__main__":
    main()
