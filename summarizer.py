import requests
import os
from dotenv import load_dotenv

load_dotenv()

def summarize_meeting(transcript: str) -> dict:
    API_KEY = os.getenv("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")
import requests

def summarize_meeting(transcript: str) -> dict:
    """Send transcript to OpenRouter (free models)"""

    API_KEY = "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"  # paste sk-or-... key here
    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""You are an expert meeting analyst. Analyze this meeting transcript and return a structured summary.

TRANSCRIPT:
{transcript}

Provide your response in this exact format:

## 📋 Meeting Summary
[2-3 sentence overview]

## ✅ Action Items
- [Person]: [Action] by [Deadline if mentioned]

## 🎯 Key Decisions
- [Decision made]

## 💡 Key Discussion Points
- [Important topic discussed]

## 👥 Participants
- [Names or roles mentioned]
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
       "model": "openrouter/free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }

    print("🤖 Sending to OpenRouter (Mistral 7B free) for analysis...")
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "choices" not in data:
        print("❌ API Error:", data)
        return {"raw": "Error from OpenRouter API"}

    summary_text = data["choices"][0]["message"]["content"]
    return {"raw": summary_text}