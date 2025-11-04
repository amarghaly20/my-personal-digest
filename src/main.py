from fetch_stock_news import get_stock_news
from summarize import summarize_text
from mailer import send_digest
import datetime

def build_digest():
    digest = []

    # Stock News
    digest.append("📊 Stock Digest:\n")
    stocks = get_stock_news(max_items=5)
    for article in stocks:
        summary = summarize_text(article)
        digest.append(f"- {summary}\n")

    return "".join(digest)

if __name__ == "__main__":
    print("⚡ Generating Personal Digest...\n")
    digest = build_digest()
    print(digest)

    subject = f"Your Personal Digest – {datetime.date.today().strftime('%b %d, %Y')}"
    send_digest(subject, digest)
    print("📧 Digest emailed successfully!")
