# sentiment_analyzer.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.25:
        return "Positive"
    elif score <= -0.25:
        return "Negative"
    else:
        return "Neutral"
