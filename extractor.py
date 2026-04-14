import requests
import json
import os
import time
from datetime import date

try:
    import streamlit as st
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_API_KEY")

MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-31b-it:free",
    "openai/gpt-oss-20b:free",
    "minimax/minimax-m2.5:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
]

def extract_structured_data(summary_text: str) -> dict:
    url = "https://openrouter.ai/api/v1/chat/completions"
    prompt = f"""Extract structured information from this meeting summary. Return ONLY valid JSON, no explanation.

MEETING SUMMARY:
{summary_text}

Return this exact JSON:
{{
  "meeting_date": "{date.today()}",
  "participants": ["name1", "name2"],
  "action_items": [
    {{
      "owner": "person name",
      "task": "what they need to do",
      "deadline": "when (or 'Not specified')"
    }}
  ],
  "key_decisions": ["decision 1"],
  "discussion_points": ["point 1"],
  "overall_summary": "2-3 sentence summary"
}}"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    for model in MODELS:
        print(f"🔍 Trying model: {model}")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            data = response.json()
            if "choices" in data:
                raw_text = data["choices"][0]["message"]["content"].strip()
                if raw_text.startswith("```"):
                    raw_text = raw_text.split("```")[1]
                    if raw_text.startswith("json"):
                        raw_text = raw_text[4:]
                return json.loads(raw_text.strip())
            else:
                print(f"❌ {model} failed: {data.get('error', {}).get('message')}")
                time.sleep(2)
        except Exception as e:
            print(f"❌ {model} error: {e}")
            time.sleep(2)

    return {}

def save_json(data: dict, path: str = "outputs/meeting_data.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Structured data saved to {path}")