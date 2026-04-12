import requests
import os

API_KEY = os.environ.get("OPENROUTER_API_KEY") or "sk-or-your-actual-key-here"
def summarize_meeting(transcript: str) -> dict:
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

    print("🤖 Sending to OpenRouter for analysis...")
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "choices" not in data:
        print("❌ API Error:", data)
        return {"raw": "Error from OpenRouter API"}

    return {"raw": data["choices"][0]["message"]["content"]}