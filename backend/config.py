# config.py
"""
Configuration for FinView backend.

For local development, you can either:
- Set environment variables, or
- Hard code temporary keys here (but NEVER commit real keys to GitHub).

Recommended:
  1. Create a file called .env (not tracked by git)
  2. Put your keys there
  3. Load them into the environment with something like python-dotenv
"""

import os

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Reddit (PRAW)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "")

if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY is not set. GPT summaries will fall back to truncated text.")

if not (REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET):
    print("WARNING: Reddit credentials are not set. Reddit scraping will fail until you configure them.")
