import whisper
import os

def extract_audio_from_video(video_path: str) -> str:
    """Extract audio from mp4 using moviepy"""
    from moviepy import VideoFileClip
    audio_path = video_path.replace(".mp4", ".wav")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
    clip.close()
    print(f"✅ Audio extracted: {audio_path}")
    return audio_path

def transcribe(file_path: str, model_size: str = "base") -> str:
    """Transcribe audio/video file using Whisper"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".mp4":
        file_path = extract_audio_from_video(file_path)

    print(f"🎙️ Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)
    print(f"🔄 Transcribing: {file_path}")
    result = model.transcribe(file_path)
    transcript = result["text"]
    print(f"✅ Done! ({len(transcript.split())} words)")
    return transcript

def load_transcript_from_text(file_path: str) -> str:
    """Load plain text transcript"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()