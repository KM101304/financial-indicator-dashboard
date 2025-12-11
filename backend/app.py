# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import re

import yfinance as yf

from reddit_scraper import scrape_reddit
from chan_scraper import scrape_4chan
from gpt_summarizer import summarize_text
from sentiment_analyzer import get_sentiment
from signal_analyzer import extract_tickers, detect_spikes

app = Flask(__name__)
CORS(app)

TICKER_PATTERN = re.compile(r"\$[A-Za-z]{1,5}")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})

@app.route("/scan", methods=["GET"])
def scan():
    logs = []
    logs.append(f"Scan started at {datetime.utcnow().isoformat()}Z")

    all_posts = []

    # --- Reddit ---
    try:
        reddit_posts = scrape_reddit(limit_per_sub=25)
        logs.append(f"Reddit posts fetched: {len(reddit_posts)}")
        all_posts.extend(reddit_posts)
    except Exception as e:
        logs.append(f"Reddit scrape error: {e}")

    # --- 4chan /biz/ ---
    try:
        chan_posts = scrape_4chan(max_threads=60)
        logs.append(f"4chan threads fetched: {len(chan_posts)}")
        all_posts.extend(chan_posts)
    except Exception as e:
        logs.append(f"4chan scrape error: {e}")

    if not all_posts:
        logs.append("No posts found from any source.")
        return jsonify({"logs": logs, "signals": [], "charts": {}})

    # Enrich posts with GPT summary + sentiment so signal_analyzer can work on them
    enriched_posts = []
    for post in all_posts:
        text_for_summary = post.get("combined") or (
            (post.get("title") or "")
            + "\n\n"
            + (post.get("snippet") or "")
        )
        summary = summarize_text(text_for_summary)
        sentiment = get_sentiment(text_for_summary)

        enriched_post = dict(post)
        enriched_post["summary"] = summary
        enriched_post["sentiment"] = sentiment
        enriched_post["_full_text"] = text_for_summary  # internal use
        enriched_posts.append(enriched_post)

    # Extract tickers and detect spikes
    tickers = extract_tickers(enriched_posts)
    unique_tickers = sorted(set(tickers))
    logs.append(f"Unique tickers mentioned: {len(unique_tickers)}")

    spikes = detect_spikes(tickers, threshold=1)
    if spikes:
        logs.append(
            "Spike tickers: " + ", ".join(
                f"{ticker} x{freq}" for ticker, freq in sorted(
                    spikes.items(), key=lambda x: x[1], reverse=True
                )
            )
        )
    else:
        logs.append("No ticker spikes detected.")

    # Build signals in the shape the frontend expects
    signals = []

    for ticker, freq in sorted(spikes.items(), key=lambda x: x[1], reverse=True):
        # Posts mentioning this ticker
        related = [
            p for p in enriched_posts
            if ticker in TICKER_PATTERN.findall(
                (p.get("_full_text") or "") + " " + (p.get("summary") or "")
            )
        ]
        if not related:
            continue

        combined_text = "\n\n".join(p["_full_text"] for p in related)
        headline = summarize_text(combined_text)

        sentiments = [p["sentiment"] for p in related]
        if sentiments:
            # majority vote
            sentiment_label = max(set(sentiments), key=sentiments.count)
        else:
            sentiment_label = "Neutral"

        sources = []
        for p in related:
            url = p.get("url")
            if url and url not in sources:
                sources.append(url)

        signals.append(
            {
                "title": f"{ticker} mentioned {freq} times across Reddit and 4chan",
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                "summary": headline,
                "sentiment": sentiment_label,
                "sources": sources,
                "spike_tickers": [ticker],
            }
        )

    # Optional: Backend charts from yfinance
    charts = {}
    for ticker in spikes.keys():
        # Frontend already fetches CoinGecko, but this is nice to have
        sym = ticker.replace("$", "")
        try:
            yf_ticker = yf.Ticker(sym)
            hist = yf_ticker.history(period="1d", interval="15m")
            if hist.empty:
                continue
            chart_data = [
                {
                    "time": idx.strftime("%H:%M"),
                    "price": float(row["Close"]),
                }
                for idx, row in hist.iterrows()
            ]
            charts[ticker] = chart_data
        except Exception as e:
            logs.append(f"Chart error for {ticker}: {e}")

    logs.append(f"Signals returned: {len(signals)}")
    logs.append(f"Charts retrieved: {len(charts)}")

    return jsonify(
        {
            "logs": logs,
            "signals": signals,
            "charts": charts,
        }
    )

if __name__ == "__main__":
    # For development
    app.run(host="0.0.0.0", port=5000, debug=True)
