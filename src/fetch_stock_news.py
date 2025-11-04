# src/fetch_stock_news.py
import requests
import os
import json
import pathlib
from dotenv import load_dotenv

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"

def get_stock_news(max_items=5):
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    keywords = config.get("stock_keywords", ["Tesla stock", "Apple stock", "AI stocks"])

    # Use stricter phrasing
    query = " OR ".join([f'"{kw}"' for kw in keywords])

    # Restrict to finance/business sources
    domains = "bloomberg.com,wsj.com,cnbc.com,reuters.com,yahoo.com"

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"sortBy=publishedAt&"  # ensures freshness
        f"language=en&"
        f"domains={domains}&"
        f"apiKey={NEWSAPI_KEY}"
    )

    print(f"🔍 Fetching stock news with query: {query}")
    resp = requests.get(url)
    data = resp.json()

    if data.get("status") != "ok":
        print("❌ NewsAPI error:", data)
        return []

    articles = data.get("articles", [])

    # Deduplicate by title
    seen = set()
    results = []
    for a in articles:
        title = a.get("title", "").strip()
        url = a.get("url", "")
        source = a.get("source", {}).get("name", "Unknown")
        published = a.get("publishedAt", "")[:10]  # YYYY-MM-DD

        # Detect which keyword matched for labeling
        label = None
        for kw in keywords:
            if kw.lower().split()[0] in title.lower():
                label = kw.split()[0]  # e.g., "Tesla" from "Tesla stock"
                break
        if not label:
            label = "General"

        if title and title not in seen:
            results.append(f"[{label} | {source}] {title} — {published} ({url})")
            seen.add(title)
        if len(results) >= max_items:
            break

    return results if results else ["⚠️ No stock news found for your keywords."]

if __name__ == "__main__":
    results = get_stock_news()
    print("📊 Stock Results:")
    for r in results:
        print("-", r)
