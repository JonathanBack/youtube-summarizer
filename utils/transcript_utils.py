"""Utility functions for handling and formatting video transcript data."""

def format_transcript(segments: list) -> list:
    """Format transcript segments into a standardized structure."""
    return [{
        "start_time": segment["start"],
        "end_time": segment["end"],
        "text": segment["text"].strip(),
    } for segment in segments]