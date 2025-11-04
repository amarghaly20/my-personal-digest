# src/fetch_science_news.py
import feedparser
import json
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"

# arXiv categories we want to cover
ARXIV_FEEDS = {
    "AI": "http://export.arxiv.org/rss/cs.AI",
    "ML": "http://export.arxiv.org/rss/cs.LG",
    "Neuroscience": "http://export.arxiv.org/rss/q-bio.NC",
    "Economics": "http://export.arxiv.org/rss/econ.EM",
    "Physics": "http://export.arxiv.org/rss/physics.comp-ph",
}

def get_science_news(max_items=5):
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    keywords = config.get("science_keywords", ["AI", "machine learning", "neuroscience"])

    print(f"🔍 Fetching science news with keywords: {keywords}")

    entries = []
    seen = set()

    # Loop through feeds
    for name, url in ARXIV_FEEDS.items():
        print(f"📡 Checking feed: {name} ({url})")
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title.strip()
            summary = entry.summary
            link = entry.link

            # Match by keyword
            if any(kw.lower() in (title + summary).lower() for kw in keywords):
                if title not in seen:
                    entries.append(f"{title} — {link}")
                    seen.add(title)

            if len(entries) >= max_items:
                break
        if len(entries) >= max_items:
            break

    return entries if entries else ["⚠️ No science articles found for your keywords."]

if __name__ == "__main__":
    results = get_science_news()
    print("🔬 Science Results:")
    for r in results:
        print("-", r)
