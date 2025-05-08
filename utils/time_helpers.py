"""Utility functions for time conversions.

This module provides functions to convert between different time formats:
- time_to_seconds: converts time string (HH:MM:SS,mmm) to seconds
- seconds_to_timestamp: converts seconds to formatted timestamp
"""

def time_to_seconds(time_str: str) -> float:
    """Convert time string (HH:MM:SS,mmm) to seconds.

    Args:
        time_str (str): Time string in format "00:00:00,000"

    Returns:
        float: Time in seconds

    """
    hours, minutes, seconds = time_str.replace(",", ".").split(":")
    return float(hours) * 3600 + float(minutes) * 60 + float(seconds)

def seconds_to_timestamp(seconds: any) -> str:
    """Convert seconds to a human-readable timestamp.

    Args:
        seconds (float): Time in seconds

    Returns:
        str: Formatted timestamp "MM:SS"

    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"
