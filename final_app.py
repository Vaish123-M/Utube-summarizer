import streamlit as st
import re
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="Login + Summarizer", layout="centered")

# In-memory user storage (temporary)
VALID_USERS = {
    "vaish@gmail.com": {"name": "Vaishnavi", "password": "mypassword123"},
    "test@example.com": {"name": "Test", "password": "test123"}
}

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Extract video ID

def extract_video_id(url):
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# Get transcript

def get_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([item['text'] for item in transcript])

# Summarize text

def summarize_text(text, length):
    summarizer = load_summarizer()
    max_len = {"Short": 60, "Medium": 120, "Long": 200}[length]
    return summarizer(text, max_length=max_len, min_length=30, do_sample=False)[0]['summary_text']

# ---------------- UI ----------------

def login_signup_ui():
    st.markdown("""
    <style>
    .container { display: flex; width: 800px; margin: 50px auto; border-radius: 20px; overflow: hidden; box-shadow: 0 0 30px rgba(0,0,0,0.1); font-family: 'Segoe UI', sans-serif; }
    .left { background: linear-gradient(to bottom right, #ff512f, #dd2476); color: white; flex: 1; padding: 50px; text-align: center; }
    .left h2 { font-size: 28px; margin-bottom: 10px; }
    .left p { font-size: 16px; margin-bottom: 30px; }
    .left button { background: transparent; border: 2px solid white; color: white; padding: 10px 25px; border-radius: 30px; font-size: 16px; cursor: pointer; }
    .right { background-color: white; flex: 1; padding: 50px; text-align: center; }
    .right h2 { font-size: 26px; margin-bottom: 20px; font-weight: bold; }
    .form-box input { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 15px; font-size: 14px; }
    .form-box button { background-color: #ff512f; color: white; width: 100%; padding: 12px; border: none; border-radius: 30px; font-weight: bold; font-size: 16px; cursor: pointer; margin-top: 10px; }
    </style>
    <div class="container">
        <div class="left">
            <h2>Welcome Back!</h2>
            <p>To keep connected with us please login<br>with your personal info.</p>
        </div>
        <div class="right">
            <h2><strong>Login</strong></h2>
    """, unsafe_allow_html=True)

    with st.form("auth_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            user = VALID_USERS.get(email)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.rerun_after_login = True
                st.success("✅ Logged in successfully! Redirecting...")
                st.stop()
            else:
                st.error("❌ Invalid email or password.")

    st.markdown("</div></div></div>", unsafe_allow_html=True)

# ---------------- MAIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

if st.session_state.get("rerun_after_login", False):
    st.session_state.rerun_after_login = False
    st.experimental_rerun()

if not st.session_state.logged_in:
    login_signup_ui()
    st.stop()

# ---------------- CUSTOM SUMMARIZER STYLES ----------------
st.markdown("""
    <style>
    .main, .block-container, .stApp {
        background-color: #ffffff !important;
        color: #121212 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3 {
        color: #6200ee !important;
        text-align: center !important;
        text-shadow: 0 0 8px #6200ee;
    }
    input[type="text"] {
        background-color: #f0f0f0 !important;
        color: #121212 !important;
        border: 1.5px solid #6200ee !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    .stButton button {
        background-color: #6200ee !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 12px 25px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(98, 0, 238, 0.7);
        transition: 0.3s ease;
    }
    .stButton button:hover {
        background-color: #3700b3 !important;
        box-shadow: 0 6px 15px #3700b3;
        cursor: pointer;
    }
    .block-container > div {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SUMMARIZER ----------------
st.markdown("<h1>🎬 YouTube Video Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Paste your YouTube video link below to get a concise summary.</p>", unsafe_allow_html=True)

left, center, right = st.columns([1, 2, 1])
with center:
    url = st.text_input("YouTube Video URL", placeholder="Enter YouTube video link here...")
    length = st.radio("Select Summary Length:", ["Short", "Medium", "Long"], index=1, horizontal=True)
    generate = st.button("Generate Summary")

    if generate:
        if url:
            try:
                with st.spinner("Fetching transcript and generating summary..."):
                    transcript = get_transcript(url)
                    if transcript:
                        summary = summarize_text(transcript, length)
                        st.success("Summary generated successfully!")
                        st.markdown(f"*Summary ({length}):* {summary}")
                    else:
                        st.error("Transcript not found for this video.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please enter a valid YouTube URL.")

# Explanation
st.markdown("""
<p style="text-align: center; max-width: 700px; margin: auto;">
A YouTube summarizer is a tool that helps users quickly understand the key points of a YouTube video by generating a concise summary. 
To use it, paste the video link and click "Generate Summary". The tool fetches the transcript and summarizes the content using AI.
</p>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Created by Vaishnavi Mamulkar | Powered by Streamlit & HuggingFace</p>", unsafe_allow_html=True)

# Sidebar Logout
with st.sidebar:
    st.write(f"👤 Logged in as: {st.session_state.user_email}")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
