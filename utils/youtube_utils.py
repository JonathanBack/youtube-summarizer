"""Utility functions for handling YouTube URLs and video IDs.

This module provides functionality to extract video IDs from various YouTube URL formats,
including standard watch URLs, shortened URLs, and embed URLs.
"""

from urllib.parse import parse_qs, urlparse


def extract_video_id(video_url: str) -> str:
    """Extract the video ID from a YouTube URL."""
    parsed_url = urlparse(video_url)

    if parsed_url.hostname in ("youtu.be", "www.youtu.be"):
        return parsed_url.path[1:]

    if parsed_url.hostname in ("youtube.com", "www.youtube.com"):
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query)["v"][0]
        if parsed_url.path.startswith("/embed/") or parsed_url.path.startswith("/v/"):
            return parsed_url.path.split("/")[2]

    msg = f"Could not extract video ID from URL: {video_url}"
    raise ValueError(msg)
