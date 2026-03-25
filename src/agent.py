import os
from logger import log_run
from deduplicator import deduplicate, mark_as_seen
import google.genai as genai
from dotenv import load_dotenv
from prompts import get_system_prompt, load_config
from fetcher import fetch_articles
from filter import filter_articles
from feeds import RSS_FEEDS

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def run_signal():
    print("--- Signal starting ---\n")
    users = load_config()

    print("Fetching articles...")
    articles = fetch_articles(RSS_FEEDS)
    print(f"Fetched {len(articles)} articles\n")

    for user in users:
        print(f"\n--- Processing for {user['name']} ---")

        fresh_articles = deduplicate(articles, user["name"])

        if not fresh_articles:
            print(f"No fresh articles for {user['name']} today.")
            continue

        print("Filtering articles...")
        passed_articles, tokens_gates12, tokens_gate3 = filter_articles(fresh_articles, user)

        if not passed_articles:
            print(f"No articles passed the filter for {user['name']} today.")
            continue

        articles_text = ""
        for article in passed_articles:
            articles_text += f"Title: {article['title']}\n"
            articles_text += f"Summary: {article['summary']}\n"
            articles_text += f"Link: {article['link']}\n\n"

        print("Generating Signal digest...")
        prompt = get_system_prompt(user, articles_text)

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents="Please process today's articles.",
            config={"system_instruction": prompt}
        )

        from delivery import send_whatsapp
        from email_delivery import send_email, format_email_html

        if user.get("delivery") == "email":
            html = format_email_html(response.text)
            send_email(
                subject=f"Signal — Your daily AI bits for {__import__('datetime').date.today().strftime('%d %B %Y')}",
                html_content=html,
                to_email=user["email"]
            )
        else:
            header = "*Signal's daily AI bits*\n\n"
            bits = response.text.split("*Bit ")
            bits = [b for b in bits if b.strip()]
            for i, bit in enumerate(bits):
                message = header if i == 0 else ""
                message += f"*Bit {bit}"
                send_whatsapp(message, user["whatsapp_number"])

        mark_as_seen(passed_articles, user["name"])

        usage = response.usage_metadata
        log_run(
            user=user,
            passed_articles=passed_articles,
            delivery_channel=user.get("delivery", "whatsapp"),
            tokens_gates12=tokens_gates12,
            tokens_gate3=tokens_gate3,
            tokens_summary={
                "input": usage.prompt_token_count,
                "output": usage.candidates_token_count
            },
            articles_fetched=len(fresh_articles),
            articles_passed=len(passed_articles)
)

run_signal()
