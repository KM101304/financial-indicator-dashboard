# reddit_scraper.py
"""
Scrapes posts and top-level comments from a few finance subreddits.
Returns a list of dicts with:
- platform: "reddit"
- subreddit
- title
- snippet       (short body)
- comments      (list of comment strings)
- combined      (title + body + comments)
- url
"""

import re
import praw
from typing import List, Dict, Any

from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
)

SUBREDDITS = ["wallstreetbets", "stocks", "investing", "cryptocurrency"]
TICKER_PATTERN = re.compile(r"\$[A-Za-z]{1,5}")

def _init_reddit() -> praw.Reddit:
    if not (REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET):
        raise RuntimeError("Reddit API credentials missing. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.")
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )

def scrape_reddit(limit_per_sub: int = 25) -> List[Dict[str, Any]]:
    reddit = _init_reddit()
    results: List[Dict[str, Any]] = []

    for sub_name in SUBREDDITS:
        try:
            subreddit = reddit.subreddit(sub_name)
            for submission in subreddit.hot(limit=limit_per_sub):
                # Filter out stickied / ads
                if getattr(submission, "stickied", False):
                    continue

                title = submission.title or ""
                body = submission.selftext or ""

                # Quick filter to skip stuff without any $TICKER-ish pattern at all
                if "$" not in title and "$" not in body:
                    continue

                # Load some comments
                submission.comments.replace_more(limit=0)
                raw_comments = submission.comments.list()[:10]
                comments = [c.body for c in raw_comments if getattr(c, "body", None)]

                combined_text = "\n\n".join(
                    [title, body] + comments
                ).strip()

                results.append(
                    {
                        "platform": "reddit",
                        "subreddit": sub_name,
                        "title": title,
                        "snippet": (body or title)[:280],
                        "comments": comments,
                        "combined": combined_text,
                        "url": f"https://www.reddit.com{submission.permalink}",
                    }
                )
        except Exception as e:
            print(f"Error scraping subreddit {sub_name}: {e}")

    return results
