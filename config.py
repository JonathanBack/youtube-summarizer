"""Configuration settings for the YouTube Video Summarizer."""
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Output directory for downloaded videos and generated transcripts
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# YouTube API settings
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Whisper model options: "tiny", "base", "small", "medium", "large"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# Gemini model
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
