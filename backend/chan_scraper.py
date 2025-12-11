# chan_scraper.py
"""
Scrapes /biz/ from 4chan via the JSON API.

Returns a list of dicts with:
- platform: "4chan"
- title
- snippet       (thread body)
- comments      (list of reply bodies)
- combined      (title + body + top replies)
- url
"""

import re
from typing import List, Dict, Any

import requests

BASE_URL = "https://a.4cdn.org/biz"
TICKER_PATTERN = re.compile(r"\$[A-Za-z]{1,5}")

def clean(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return (
        text.replace("<br>", "\n")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#039;", "'")
    )

def scrape_4chan(max_threads: int = 80) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    try:
        catalog = requests.get(f"{BASE_URL}/catalog.json", timeout=10).json()
    except Exception as e:
        print("Error fetching 4chan catalog:", e)
        return results

    threads_processed = 0

    for page in catalog:
        for thread in page.get("threads", []):
            if threads_processed >= max_threads:
                return results

            thread_id = thread.get("no")
            if not thread_id:
                continue

            title = clean(thread.get("sub", "") or "")
            body = clean(thread.get("com", "") or "")

            # Quick filter: skip threads with no dollar signs at all
            if "$" not in title and "$" not in body:
                continue

            try:
                thread_json = requests.get(
                    f"{BASE_URL}/thread/{thread_id}.json", timeout=10
                ).json()
                posts = thread_json.get("posts", [])
                # first post is the OP
                replies = []
                for post in posts[1:11]:
                    if "com" in post:
                        replies.append(clean(post["com"]))

                combined_text = "\n\n".join(
                    [title or "Untitled Thread", body] + replies
                ).strip()

                results.append(
                    {
                        "platform": "4chan",
                        "title": title or "Untitled Thread",
                        "snippet": body[:280],
                        "comments": replies,
                        "combined": combined_text,
                        "url": f"https://boards.4channel.org/biz/thread/{thread_id}",
                    }
                )
                threads_processed += 1
            except Exception as e:
                print(f"Error loading thread {thread_id}: {e}")

    return results
