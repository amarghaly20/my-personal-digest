import requests
import os
import json
import pathlib
from dotenv import load_dotenv
from urllib.parse import quote_plus
from difflib import SequenceMatcher
import re

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"

def normalize_title(title):
    """Lowercase, remove punctuation, normalize spaces"""
    title = title.lower()
    title = re.sub(r"[^a-z0-9 ]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title

def is_similar(a, b, threshold=0.85):
    """Return True if two titles are similar above threshold"""
    return SequenceMatcher(None, a, b).ratio() > threshold

def get_stock_news(max_items=5):
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    keywords = config.get("stock_keywords", ["Tesla stock", "Apple stock", "AI stocks"])

    # Build query and URL-encode
    query = " OR ".join([f'"{kw}"' for kw in keywords])
    encoded_query = quote_plus(query)

    # Restrict to finance/business sources
    domains = "bloomberg.com,wsj.com,cnbc.com,reuters.com,yahoo.com"

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={encoded_query}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"domains={domains}&"
        f"apiKey={NEWSAPI_KEY}"
    )

    print(f"🔍 Fetching stock news with query: {query}")

    try:
        resp = requests.get(url)
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print("❌ Network error:", e)
        return []

    if data.get("status") != "ok":
        print("❌ NewsAPI error:", data)
        return []

    articles = data.get("articles", [])

    # Deduplicate by normalized/fuzzy titles
    seen = []
    results = []

    for a in articles:
        title = a.get("title", "").strip()
        article_url = a.get("url", "")
        source = a.get("source", {}).get("name", "Unknown")
        published = a.get("publishedAt", "")[:10]

        if not title:
            continue

        norm_title = normalize_title(title)

        if any(is_similar(norm_title, t) for t in seen):
            continue  # skip duplicates
        seen.append(norm_title)

        # Detect which keyword matched for labeling
        label = "General"
        for kw in keywords:
            if kw.lower().split()[0] in title.lower():
                label = kw.split()[0]
                break

        results.append(f"[{label} | {source}] {title} — {published} ({article_url})")

        if len(results) >= max_items:
            break

    return results if results else ["⚠️ No stock news found for your keywords."]

if __name__ == "__main__":
    results = get_stock_news()
    print("📊 Stock Results:")
    for r in results:
        print("-", r)