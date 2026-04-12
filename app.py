import streamlit as st
import os
import json
import tempfile
from summarizer import summarize_meeting
from extractor import extract_structured_data, save_json
from transcriber import transcribe, load_transcript_from_text

os.makedirs("outputs", exist_ok=True)

st.set_page_config(page_title="AI Meeting Summarizer", page_icon="🎙️", layout="wide")

st.title("🎙️ AI Meeting Summarizer")
st.caption("Upload your meeting file and get instant AI-powered summary")

uploaded_file = st.file_uploader("Upload Meeting File", type=["mp3", "wav", "mp4", "txt"])

if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")

    if st.button("🚀 Analyze Meeting", type="primary", use_container_width=True):
        suffix = os.path.splitext(uploaded_file.name)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with st.spinner("📝 Transcribing..."):
            if suffix == ".txt":
                transcript = load_transcript_from_text(tmp_path)
            else:
                transcript = transcribe(tmp_path, model_size="base")

        with st.spinner("🤖 Summarizing with AI..."):
            result = summarize_meeting(transcript)

        with st.spinner("🔍 Extracting structured data..."):
            structured = extract_structured_data(result["raw"])

        st.success("🎉 Done!")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Participants", len(structured.get("participants", [])))
        col2.metric("✅ Action Items", len(structured.get("action_items", [])))
        col3.metric("🎯 Decisions", len(structured.get("key_decisions", [])))
        col4.metric("💬 Topics", len(structured.get("discussion_points", [])))

        st.markdown("---")
        st.markdown("### 📋 Summary")
        st.write(structured.get("overall_summary", result["raw"]))

        st.markdown("### ✅ Action Items")
        for item in structured.get("action_items", []):
            st.info(f"**{item.get('owner')}** → {item.get('task')} | ⏰ {item.get('deadline')}")

        st.markdown("### 🎯 Key Decisions")
        for d in structured.get("key_decisions", []):
            st.success(d)

        st.markdown("### 👥 Participants")
        st.write(", ".join(structured.get("participants", [])))

        st.markdown("---")
        st.markdown("### 💾 Downloads")
        c1, c2, c3 = st.columns(3)
        c1.download_button("📄 Transcript", transcript, file_name="transcript.txt")
        c2.download_button("📊 Summary", result["raw"], file_name="summary.txt")
        c3.download_button("🗂️ JSON", json.dumps(structured, indent=2), file_name="meeting_data.json")

        os.unlink(tmp_path)