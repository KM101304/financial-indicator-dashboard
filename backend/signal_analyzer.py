# signal_analyzer.py
from collections import Counter
import re

def extract_tickers(posts):
    tickers = []
    pattern = re.compile(r'\$[A-Za-z]{1,5}')

    for post in posts:
        if "title" in post:
            tickers += pattern.findall(post["title"])
        if "summary" in post:
            tickers += pattern.findall(post["summary"])
        if "snippet" in post:
            tickers += pattern.findall(post["snippet"])

    return tickers

def detect_spikes(tickers, threshold=1):
    count = Counter(tickers)
    spikes = {ticker: freq for ticker, freq in count.items() if freq >= threshold}
    return spikes
