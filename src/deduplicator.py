import json
import os

SEEN_FILE = "seen_articles.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    return {}

def save_seen(seen_data):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen_data, f, indent=2)

def deduplicate(articles, user_name):
    seen = load_seen()
    user_seen = seen.get(user_name, [])
    fresh = [a for a in articles if a["link"] not in user_seen]
    print(f"Deduplication for {user_name}: {len(articles)} fetched, {len(fresh)} fresh, {len(articles) - len(fresh)} already seen")
    return fresh

def mark_as_seen(articles, user_name):
    seen = load_seen()
    user_seen = seen.get(user_name, [])
    new_links = [a["link"] for a in articles]
    seen[user_name] = list(set(user_seen + new_links))
    save_seen(seen)
    print(f"Marked {len(new_links)} articles as seen for {user_name}. Total seen: {len(seen[user_name])}")