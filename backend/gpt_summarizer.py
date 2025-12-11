# gpt_summarizer.py
import openai
from config import OPENAI_API_KEY

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
else:
    openai.api_key = None

def summarize_text(text: str) -> str:
    """
    Summarize a long chunk of text into a short, clear headline
    suitable for a financial dashboard.
    """
    if not OPENAI_API_KEY:
        # Fallback: no API key configured
        return (text or "")[:140] + "..."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial news summarizer. "
                        "Given discussion text from Reddit / 4chan about crypto or stocks, "
                        "return a short, punchy headline (max ~20 words) that captures "
                        "the main market-relevant idea."
                    ),
                },
                {"role": "user", "content": text},
            ],
            max_tokens=60,
            temperature=0.4,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print("GPT error:", e)
        return (text or "")[:140] + "..."
