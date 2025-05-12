"""Entry point for the YouTube Video Summarizer application."""
import argparse
import logging
import sys

from utils.summarizer import generate_summary
from utils.timestamp_generator import generate_timestamps
from utils.whisper_transcriber import transcribe_audio
from utils.youtube_api import get_video_transcript
from utils.youtube_dl_wrapper import download_video

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="YouTube Video Summarizer")
    parser.add_argument("video_url", help="URL of the YouTube video to summarize")
    parser.add_argument(
        "--method",
        choices=["api", "download"],
        default="api",
        help="Method to obtain transcription: 'api' (YouTube API) or 'download' (youtube-dl + Whisper)"
    )
    parser.add_argument(
        "--force-download", 
        action="store_true",
        help="Force download and transcription even if API transcription is available"
    )
    return parser.parse_args()

def main():
    """Execute the main program function."""
    args = parse_arguments()
    video_url = args.video_url
    method = args.method
    force_download = args.force_download

    logger.info("Processing video: %s", video_url)
    # Try to get transcript via youtube-transcript-api first (unless forced to download)
    transcript = None
    if method == "api" and not force_download:
        try:
            logger.info("Attempting to fetch transcript via youtube-transcript-api...")
            transcript = get_video_transcript(video_url)
            if transcript:
                logger.info("Successfully retrieved transcript from youtube-transcript-api")
        except (ValueError, KeyError, ConnectionError) as e:
            logger.warning("Failed to get transcript via youtube-transcript-api: %s", e)
            if method == "api":
                logger.info("Falling back to download method")

    # If transcript not available or download method selected
    if transcript is None or force_download or method == "download":
        logger.info("Using youtube-dl to download video...")
        audio_file = download_video(video_url)

        if audio_file:
            logger.info("Downloaded audio to %s", audio_file)
            logger.info("Transcribing with Whisper...")
            transcript = transcribe_audio(audio_file)
            logger.info("Transcription complete")
        else:
            logger.error("Failed to download video")
            return

    # Generate timestamps
    logger.info("Generating timestamps...")
    timestamps = generate_timestamps(transcript)

    # Generate summary
    logger.info("Generating summary with Gemini API...")
    summary = generate_summary(transcript, timestamps)

    # Print results
    print("\n=== VIDEO SUMMARY ===\n")
    print(summary)

    logger.info("Summary generation complete!")

if __name__ == "__main__":
    main()
