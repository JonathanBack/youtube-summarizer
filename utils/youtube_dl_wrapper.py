"""Module for downloading YouTube videos using youtube-dl."""
import logging
from pathlib import Path

import youtube_dl

import config
from utils.youtube_api import extract_video_id

logger = logging.getLogger(__name__)

def download_video(video_url: str) -> str | None:
    """Download a YouTube video and extract its audio.

    Args:
        video_url: URL of the YouTube video

    Returns:
        str: Path to the extracted audio file, or None if download fails

    """
    # Create a unique filename based on video ID
    video_id = extract_video_id(video_url)
    output_path = Path(config.OUTPUT_DIR) / video_id
    audio_path = f"{output_path}.mp3"

    # Skip download if audio file already exists
    if Path(audio_path).exists():
        logger.info("Audio file already exists: %s", audio_path)
        return audio_path

    # youtube-dl options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{output_path}.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        logger.exception("Error downloading video.")
        return None
    else:
        logger.info("Successfully downloaded and converted to MP3: %s", audio_path)
        return audio_path
