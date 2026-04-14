import requests
import os
import time

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

    for model in MODELS:
        print(f"🤖 Trying model: {model}")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            data = response.json()
            if "choices" in data:
                print(f"✅ Success with {model}")
                return {"raw": data["choices"][0]["message"]["content"]}
            else:
                print(f"❌ {model} failed: {data.get('error', {}).get('message')}")
                time.sleep(2)
        except Exception as e:
            print(f"❌ {model} error: {e}")
            time.sleep(2)

    return {"raw": "Error from OpenRouter API"}