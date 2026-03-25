import json
import os
from datetime import datetime

LOG_FILE = "signal_log.json"

def log_run(user, passed_articles, delivery_channel,
            tokens_gates12, tokens_gate3, tokens_summary,
            articles_fetched, articles_passed):

    def ratio(inp, out):
        return round(inp / out, 2) if out > 0 else 0

    entry = {
        "run_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "user": {
            "name": user["name"],
            "learning_layer": user["learning_layer"],
            "learning_goal": user["learning_goal"],
            "delivery_channel": delivery_channel
        },
        "articles_delivered": [
            {
                "bit_number": i + 1,
                "title": article["title"],
                "source_url": article["link"],
                "source_domain": article["link"].split("/")[2] if article["link"] else "unknown"
            }
            for i, article in enumerate(passed_articles)
        ],
        "user_feedback": None,
        "filter_stats": {
            "fetched": articles_fetched,
            "passed": articles_passed,
            "pass_rate_pct": round(articles_passed / articles_fetched * 100, 1) if articles_fetched > 0 else 0
        },
        "token_breakdown": {
            "gates_12_gemma3": {
                "model": "gemma-3-12b-it",
                "input": tokens_gates12["input"],
                "output": tokens_gates12["output"],
                "total": tokens_gates12["input"] + tokens_gates12["output"],
                "ratio": ratio(tokens_gates12["input"], tokens_gates12["output"])
            },
            "gate_3_flash_lite": {
                "model": "gemini-2.5-flash-lite",
                "input": tokens_gate3["input"],
                "output": tokens_gate3["output"],
                "total": tokens_gate3["input"] + tokens_gate3["output"],
                "ratio": ratio(tokens_gate3["input"], tokens_gate3["output"])
            },
            "summarisation_flash": {
                "model": "gemini-2.5-flash",
                "input": tokens_summary["input"],
                "output": tokens_summary["output"],
                "total": tokens_summary["input"] + tokens_summary["output"],
                "ratio": ratio(tokens_summary["input"], tokens_summary["output"])
            },
            "overall": {
                "input": tokens_gates12["input"] + tokens_gate3["input"] + tokens_summary["input"],
                "output": tokens_gates12["output"] + tokens_gate3["output"] + tokens_summary["output"],
                "total": (tokens_gates12["input"] + tokens_gates12["output"] +
                          tokens_gate3["input"] + tokens_gate3["output"] +
                          tokens_summary["input"] + tokens_summary["output"]),
                "ratio": ratio(
                    tokens_gates12["input"] + tokens_gate3["input"] + tokens_summary["input"],
                    tokens_gates12["output"] + tokens_gate3["output"] + tokens_summary["output"]
                )
            }
        }
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"\n--- Run Logged ---")
    print(f"Run ID: {entry['run_id']}")
    print(f"User: {user['name']} | Layer: {user['learning_layer']} | Channel: {delivery_channel}")
    print(f"Filter: {articles_fetched} fetched → {articles_passed} passed ({entry['filter_stats']['pass_rate_pct']}%)")
    print(f"Tokens — Gemma3 (G1+2): {tokens_gates12['input']}in/{tokens_gates12['output']}out | "
          f"FlashLite (G3): {tokens_gate3['input']}in/{tokens_gate3['output']}out | "
          f"Flash (summary): {tokens_summary['input']}in/{tokens_summary['output']}out")
    print(f"Overall ratio: {entry['token_breakdown']['overall']['ratio']}:1")