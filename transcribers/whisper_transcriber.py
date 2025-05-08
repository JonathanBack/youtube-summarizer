"""Transcriber implementation that uses youtube-dl and OpenAI's Whisper."""

import json
import logging
import os

import config
import whisper
import youtube_dl

from transcribers.base_transcriber import BaseTranscriber
from utils.file_utils import file_exists, load_json, save_json
from utils.transcript_utils import format_transcript
from utils.youtube_utils import extract_video_id

logger = logging.getLogger(__name__)

class WhisperTranscriber(BaseTranscriber):
    """Downloads videos and transcribes them using OpenAI's Whisper model."""

    def __innit_(self) -> None:
        """Initialize the Whisper transcriber."""
        pass

        def get_transcript(self, video_url: str) -> list:
            """Download a video and transcriber it using Whisper".

            Args:
                video_url (str): URL of the video

            Returns:
                list: Transcript data with timestamps

            """
            # Download the video first
            audio_file = self.download_video(video_url)

            if not audio_file:
                msg = f"Failed to downnload video: {video_url}"
                raise RuntimeError(msg)

            # Transcribe the audio
            return self._transcribe_audio(audio_file)



    def _download_video(self, video_url: str) -> str:
        """Download a YouTube video and extract its audio.

        Args:
            video_url (str): URL of the YouTube video

        Returns:
            str: Path to the extracted audio file

        """
        # Create a unique filename based on video ID
        video_id = extract_video_id(video_url)  # Use utility function
        output_path = os.path.join(config.OUTPUT_DIR, video_id)
        audio_path = f"{output_path}.mp3"

        # Skip download if audio file already exists
        if os.path.exists(audio_path):
            logger.info(f"Audio file already exists: {audio_path}")
            return audio_path

        # youtube-dl options
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{output_path}.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": False,
            "no_warnings": False,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            logger.info(f"Successfully donwloaded and converted to MP3: {audio_path}")
            return audio_path
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None

    def _transcribe_audio(self, audio_file: str) -> list:
        """Transcribe the audio file using Whisper.

        Args:
            audio_file (str): Path to the audio file

        Returns:
            list: Transcript data with timestamps

        """
        # Generate transcript output path
        transcript_path = f"{os.path.splitext(audio_file)[0]}_transcript.json"

        # Skip transcription if transcript file already exists
        if file_exists(transcript_path):  # Use utility function
            logger.info(f"Loading existing transcript: {transcript_path}")
            return load_json(transcript_path)

        # Load the Whisper model
        logger.info(f"Loading Whisper model: {config.WHISPER_MODEL}")
        model = whisper.load_model(config.WHISPER_MODEL)

        # Transcribe audio
        logger.info("Transcribing audio with Whisper...")
        result = model.transcribe(
            audio_file,
            fp16=False, # Set to True if using a GPU with FP16 support
            verbose=True
        )

        # Format transcript
        transcript = format_transcript(result["segments"])  # Use utility function

        # Save transcript to file
        save_json(transcript, transcript_path)  # Use utility function

        logger.info(f"Transcript saved to: {transcript_path}")
        return transcript
