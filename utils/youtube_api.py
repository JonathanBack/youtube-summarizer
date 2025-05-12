"""Module for interacting with YouTube."""

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled


def extract_video_id(video_url: str) -> str:
    """Extract the video ID from a YouTube URL using pytube.

    Args:
        video_url (str): The full YouTube video URL.

    Returns:
        str: The video ID.

    Raises:
        ValueError: If the video ID cannot be extracted.

    """
    try:
        yt = YouTube(video_url)
    except Exception as e:
        msg = f"Could not extract video ID from URL: {video_url}. Error: {e}"
        raise ValueError(msg) from e
    else:
        return yt.video_id

def get_video_transcript(video_url: str) -> list:
    """Get the transcript of a YouTube video using youtube-transcript-api.

    Args:
        video_url (str): URL of the YouTube video.

    Returns:
        list: List of transcript segments, where each segment contains:
              - 'start': Start time in seconds
              - 'duration': Duration in seconds
              - 'text': Transcript text.

    Raises:
        ValueError: If the transcript cannot be retrieved.

    """
    video_id = extract_video_id(video_url)  # Use the existing extract_video_id function

    try:
        # Fetch the transcript using youtube-transcript-api
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
    except TranscriptsDisabled as disabled:
        msg = f"Transcripts are disabled for video ID: {video_id}"
        raise ValueError(msg) from disabled
    except NoTranscriptFound as no_transcript:
        msg = f"No transcript found for video ID: {video_id}"
        raise ValueError(msg) from no_transcript
    except Exception as e:
        msg = f"An error occurred while fetching the transcript: {e}"
        raise ValueError(msg) from e
    else:
        return transcript
