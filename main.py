"""Entry point for the YouTube Video Summarizer application."""
import argparse
import logging
import sys

import config
from processors.video_processor import VideoProcessor

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
    """Main execution function."""
    args = parse_arguments()

    logger.info(f"Processing video: {args.video_url}")

    # Initialize the video processor
    processor = VideoProcessor(args.video_url)

    # Process the video and get the summary
    summary = processor.process(
        method=args.method,
        force_download=args.force_download
    )

    # Print results
    print("\n=== VIDEO SUMMARY ===\n")
    print(summary)

    logger.info("Summary generation complete!")

if __name__ == "__main__":
    main()
