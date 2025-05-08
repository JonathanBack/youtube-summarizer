"""Main processor class for handling YouTube video summarization."""

import logging

from processors.summary_generator import SummaryGenerator
from processors.timestamp_generator import TimestampGenerator
from transcribers.whisper_transcriber import WhisperTranscriber
from transcribers.youtube_api_transcriber import YouTubeAPITranscriber
from utils.time_helpers import seconds_to_timestamp, time_to_seconds
from utils.transcript_utils import format_transcript
from utils.youtube_utils import extract_video_id

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Main class that orchestrates the video processing pipeline."""

    def __init__(self, video_url: str) -> None:
        """Initialize a new VideoProcessor.

        Args:
            video_url (str): URL of the YouTube video to process

        """
        self.video_url = video_url
        self.video_id = extract_video_id(video_url)  # Use the utility function
        self.transcript = None
        self.timestamps = None
        self.summary = None

        # Initialize components
        self.api_transcriber = YouTubeAPITranscriber()
        self.whisper_transcriber = WhisperTranscriber()
        self.timestamp_generator = TimestampGenerator()
        self.summary_generator = SummaryGenerator()

    def process(self, method="api", force_download=False):
        """Process the video to generate a summary.

        Args:
            method (str): Method to obtain transcription: 'api' or 'download'
            force_download (bool): Force download even if API transcription is available

        Returns:
            str: Generated summary

        """
        self._get_transcript(method, force_download)
        self._generate_timestamps()
        self._generate_summary()
        return self.summary

    def _get_transcript(self, method, force_download):
        """Get the transcript using the specified method."""
        transcript = None

        # Try YouTube API first if specified and not forcing download
        if method == "api" and not force_download:
            try:
                logger.info("Attempting to fetch transcript via YouTube API...")
                transcript = self.api_transcriber.get_transcript(self.video_url)
                if transcript:
                    logger.info("Successfully retrieved transcript from YouTube API")
                    self.transcript = transcript
                    return
            except Exception as e:
                logger.warning(f"Failed to get transcript via API: {e}")
                if method == "api":
                    logger.info("Falling back to download method")

        # Use Whisper transcription if API failed or download was specified
        logger.info("Using youtube-dl and Whisper for transcription...")
        transcript = self.whisper_transcriber.get_transcript(self.video_url)

        if transcript:
            logger.info("Whisper transcription complete")
            self.transcript = transcript
        else:
            logger.error("Failed to obtain transcript")
            raise RuntimeError("Could not obtain transcript through any method")

    def _generate_timestamps(self) -> None:
        """Generate timestamps from the transcript."""
        if not self.transcript:
            raise ValueError("No transcript available for timestamp generation")

        logger.info("Generating timestamps...")
        self.timestamps = self.timestamp_generator.generate(self.transcript)
        logger.info(f"Generated {len(self.timestamps)} key timestamps")

    def _generate_summary(self):
        """Generate summary from the transcript and timestamps."""
        if not self.transcript or not self.timestamps:
            raise ValueError(
                "Transcript and timestamps required for summary generation"
            )

        logger.info("Generating summary...")
        self.summary = self.summary_generator.generate(self.transcript, self.timestamps)
        logger.info("Summary generation complete")
