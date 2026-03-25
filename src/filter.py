import os
import json
import re
import time
import google.genai as genai
from dotenv import load_dotenv

GATE_12_MODEL = "models/gemma-3-12b-it"
GATE_3_MODEL = "models/gemini-2.5-flash-lite"

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def filter_article(article, config):
    prompt_12 = f"""
You are a content filter for a personalised AI learning agent.
Evaluate this article against the user profile.

User profile:
- Learning goal: {config["learning_goal"]}
- Knowledge level: {config["knowledge_level"]}
- Current learning layer: {config["learning_layer"]}
- Topic interests: {config["topic_interests"]}

Article:
Title: {article["title"]}
Summary: {article["summary"]}

Gate 1 — Relevance: Does this article relate to the user's learning goal and topic interests?
Gate 2 — Level: Is this appropriate for their knowledge level and learning layer? Allow current layer and one layer above. Reject anything below.

Respond in this exact JSON format and nothing else:
{{
  "pass": true or false,
  "gate_failed": null or 1 or 2,
  "reason": "one sentence explanation"
}}
"""

    response_12 = client.models.generate_content(
        model=GATE_12_MODEL,
        contents=prompt_12
    )

    raw = response_12.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    result_12 = json.loads(raw)

    tokens_12 = {
        "input": response_12.usage_metadata.prompt_token_count or 0,
        "output": response_12.usage_metadata.candidates_token_count or 0
    }

    if not result_12["pass"]:
        result_12["tokens_gates12"] = tokens_12
        result_12["tokens_gate3"] = {"input": 0, "output": 0}
        return result_12

    prompt_3 = f"""
You are a content filter for a personalised AI learning agent.

Article:
Title: {article["title"]}
Summary: {article["summary"]}

Gate 3 — Signal value: Think step by step. Does this teach something genuinely useful or is it noise, clickbait, or generic commentary?

Respond in this exact JSON format and nothing else:
{{
  "pass": true or false,
  "gate_failed": null or 3,
  "reason": "one sentence explanation"
}}
"""

    response_3 = client.models.generate_content(
        model=GATE_3_MODEL,
        contents=prompt_3
    )

    raw = response_3.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    result_3 = json.loads(raw)

    result_3["tokens_gates12"] = tokens_12
    result_3["tokens_gate3"] = {
        "input": response_3.usage_metadata.prompt_token_count or 0,
        "output": response_3.usage_metadata.candidates_token_count or 0
    }
    return result_3


def filter_article_with_retry(article, config, max_retries=3):
    for attempt in range(max_retries):
        try:
            return filter_article(article, config)
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = 30 * (attempt + 1)
                print(f"Rate limit hit. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                time.sleep(wait_time)
            else:
                raise


def filter_articles(articles, config):
    passed = []
    rejected = []
    total_tokens_gates12 = {"input": 0, "output": 0}
    total_tokens_gate3 = {"input": 0, "output": 0}

    for article in articles:
        print(f"Filtering: {article['title'][:60]}...")
        result = filter_article_with_retry(article, config)

        total_tokens_gates12["input"] += result.get("tokens_gates12", {}).get("input", 0)
        total_tokens_gates12["output"] += result.get("tokens_gates12", {}).get("output", 0)
        total_tokens_gate3["input"] += result.get("tokens_gate3", {}).get("input", 0)
        total_tokens_gate3["output"] += result.get("tokens_gate3", {}).get("output", 0)

        if result["pass"]:
            passed.append(article)
            print(f"  PASS — {result['reason']}")
        else:
            rejected.append(article)
            print(f"  FAIL (Gate {result['gate_failed']}) — {result['reason']}")

        if len(passed) == 3:
            break

    print(f"\nFilter summary: {len(passed)} passed, {len(rejected)} rejected")
    return passed, total_tokens_gates12, total_tokens_gate3