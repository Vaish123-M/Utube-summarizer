import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Configure API Key
genai.configure(api_key=os.getenv("AIzaSyBxbe1zPVuDsGZZWZQu8TdXFVV5xmjVf84"))

# Initialize Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- Login Section ---
def login():
    st.title("🔐 YouTube Summarizer Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "pass123":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials. Try again.")

# --- Summarizer Section ---
def summarize():
    st.title("📽️ YouTube Summarizer with Gemini AI")

    yt_url = st.text_input("Paste YouTube Video Link")

    if st.button("Summarize"):
        try:
            video_id = yt_url.split("v=")[-1].split("&")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = " ".join([entry['text'] for entry in transcript])

            short_text = text[:3000]  # trim to stay under quota
            with st.spinner("Summarizing..."):
                response = model.generate_content(f"Summarize this transcript: {short_text}")
                st.subheader("📝 Summary")
                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

# --- Main App Logic ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    summarize()
else:
    login()
