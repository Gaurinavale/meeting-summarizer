import requests
import json
import os
from datetime import date

try:
    import streamlit as st
    API_KEY = st.secrets["notepad C:\meeting-summarizer\extractor.py"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("notepad C:\meeting-summarizer\extractor.py")


def extract_structured_data(summary_text: str) -> dict:
    """Send summary to AI and get clean structured JSON"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""You are a data extraction expert. Extract structured information from this meeting summary and return ONLY a valid JSON object. No explanation, no markdown, just raw JSON.

MEETING SUMMARY:
{summary_text}

Return this exact JSON structure:
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
  "key_decisions": ["decision 1", "decision 2"],
  "discussion_points": ["point 1", "point 2"],
  "overall_summary": "2-3 sentence summary"
}}"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }

    print("🔍 Extracting structured data...")
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "choices" not in data:
        print("❌ API Error:", data)
        return {}

    raw_text = data["choices"][0]["message"]["content"]

    raw_text = raw_text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]

    structured = json.loads(raw_text.strip())
    return structured


def save_json(data: dict, path: str = "outputs/meeting_data.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Structured data saved to {path}")