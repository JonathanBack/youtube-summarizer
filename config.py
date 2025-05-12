"""Configuration settings for the YouTube Video Summarizer."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Output directory for downloaded videos and generated transcripts
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# Output directory for downloaded videos and generated transcripts
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
OUTPUT_DIR.mkdir(exist_ok=True)

# Whisper model options: "tiny", "base", "small", "medium", "large"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# Gemini model
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
