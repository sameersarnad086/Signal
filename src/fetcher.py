import feedparser
import random

def fetch_articles(feed_urls):
    articles = []
    shuffled_urls = random.sample(feed_urls, len(feed_urls))
    for url in shuffled_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")
            })
    return articles