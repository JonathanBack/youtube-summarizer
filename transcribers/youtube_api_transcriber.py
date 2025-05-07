"""Transcriber implementation that uses the YouTube Data API."""

import logging
import re
from urllib.parse import parse_qs, urlparse

import config
import googleapiclient.discovery

from transcribers.base_transcriber import BaseTranscriber

logger = logging.getLogger(__name__)

class YouTubeAPITranscriber(BaseTranscriber):
    """Obtains transcripts using the YouTube Data API."""

    def _innit__(self) -> None:
        """Initialize the YouTube API transcriber."""
        pass

    def get_transcript(self, video_url: str) -> list:
        """Get the transcript of a YouTube video using the YouTube Data API.

        Args:
            video_url (str): URL of the video
        Returns:
            list: List of transcript segments with timestamps

        """
        video_id = self.extract_video_id(video_url)

        # Build the YouTube service
        youtube = googleapiclient.discovery.build(
            config.YOUTUBE_API_SERVICE_NAME,
            config.YOUTUBE_API_VERSION,
            developerKey=config.YOUTUBE_API_KEY)

        # Get video captions
        results = youtube.captions().list(
            part="snippet",
            videoId=video_id).execute()

        captions = results.get("items", [])
        if not captions:
            msg = f"No captions found for video ID: {video_id}"
            raise ValueError(msg)

        # Get the first available caption track (preferably English)
        caption_id = None
        for caption in captions:
            if caption["snippet"]["language"] == "en":
                caption_id = caption["id"]
                break

        # If no English caption track is found, use the first one
        if not caption_id and captions:
            caption_id = captions[0]["id"]

        # Download the caption track
        subtitle = youtube.captions().download(
            id=caption_id,
            tfmt="srt").execute()

        # Parse the SRT format and convert to transcript dict
        return self.parse_srt(subtitle.decode("utf-8"))

    def _extract_video_id(self, video_url: str) -> str:
        """Extract the video ID from a YouTube URL.

        Args:
            video_url (str): URL of the video

        Returns:
            str: Video ID

        """
        parsed_url = urlparse(video_url)

        if parsed_url.hostname in ("youtu.be", "www.youtu.be"):
            return parsed_url.path[1:]

        if parsed_url.hostname in ("youtube.com", "www.youtube.com"):
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query)["v"][0]
            if parsed_url.path.startswith("/embed/") or parsed_url.path.startswith("/v/"):
                return parsed_url.path.split("/")[2]

        # If nothing matched
        msg = f"Could not extract video ID from URL: {video_url}"
        raise ValueError(msg)

    def _parse_srt(self, srt_string: str) -> list:
        """Parse SRT formatted subtitle string into a structure transcript.

        Args:
            srt_string (str): String in SRT format

        Returns:
            list: List of dicts with start_time, end_time and text

        """
        transcript = []
        pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?)(?=\n\n|\Z)")  # noqa: E501

        matches = pattern.findall(srt_string)
        for _, start_time, end_time, text in matches:
            # Convert time format from "00:00:00,000" to seconds
            start_seconds = self._time_to_seconds(start_time)
            end_seconds = self._time_to_seconds(end_time)

            transcript.append({
                "start_time": start_seconds,
                "end_time": end_seconds,
                "text": text.strip().replace("\n", " ")
            })

        return transcript

    def _time_to_seconds(self, time_str: str) -> float:
        """Convert time string in "HH:MM:SS,mmm" format to seconds.

        Args:
            time_str (str): Time string

        Returns:
            float: Time in seconds

        """
        hours, minutes, seconds = time_str.replace(",", ".").split(":")
        return float(hours) * 3600 + float(minutes) * 60 + float(seconds)