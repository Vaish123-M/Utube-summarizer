from dotenv import load_dotenv
import os
import google.generativeai as genai

# ✅ Load .env and configure Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# ✅ Load summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def extract_transcript(video_url):
    try:
        # ✅ Extract video ID more safely (some links have &t= or other params)
        if "v=" in video_url:
            video_id = video_url.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[-1].split("?")[0]
        else:
            return "Error: Invalid YouTube URL"

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item["text"] for item in transcript])
        return text
    except Exception as e:
        return f"Error: {e}"

def summarize_text(text):
    try:
        # transformers pipeline has a token limit (~1024 tokens)
        if len(text) > 1000:
            text = text[:1000]
        summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error during summarization: {e}"
