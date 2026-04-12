from transcriber import transcribe, load_transcript_from_text
from summarizer import summarize_meeting
from extractor import extract_structured_data, save_json
import os
import json

def get_transcript(input_path: str) -> str:
    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".txt":
        return load_transcript_from_text(input_path)
    else:
        return transcribe(input_path, model_size="base")

if __name__ == "__main__":
    input_path = "meeting.txt"

    print("=" * 50)
    print("🎙️  AI MEETING SUMMARIZER")
    print("=" * 50)

    # Step 1: Transcribe
    print("\n📝 Step 1: Getting transcript...")
    transcript = get_transcript(input_path)
    with open("outputs/transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)
    print("💾 Transcript saved!")

    # Step 2: Summarize
    print("\n🤖 Step 2: Summarizing with AI...")
    result = summarize_meeting(transcript)
    with open("outputs/summary.txt", "w", encoding="utf-8") as f:
        f.write(result["raw"])
    print("💾 Summary saved!")

    # Step 3: Extract structured JSON
    print("\n🔍 Step 3: Extracting structured data...")
    structured = extract_structured_data(result["raw"])
    save_json(structured)

    # Step 4: Print everything nicely
    print("\n" + "=" * 50)
    print("📊 MEETING SUMMARY")
    print("=" * 50)
    print(result["raw"])

    print("\n" + "=" * 50)
    print("📋 STRUCTURED DATA")
    print("=" * 50)
    print(f"📅 Date: {structured.get('meeting_date', 'N/A')}")
    print(f"👥 Participants: {', '.join(structured.get('participants', []))}")

    print("\n✅ Action Items:")
    for item in structured.get("action_items", []):
        print(f"   • {item['owner']}: {item['task']} → by {item['deadline']}")

    print("\n🎯 Key Decisions:")
    for d in structured.get("key_decisions", []):
        print(f"   • {d}")

    print("\n✅ All outputs saved to outputs/ folder!")