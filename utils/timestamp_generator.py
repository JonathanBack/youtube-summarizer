"""Module for generating timestamps with key points from transcripts."""
import logging
import re

import google.generativeai as genai

import config

logger = logging.getLogger(__name__)

def generate_timestamps(transcript : list) -> list:
    """Generate timestamps with key points from a transcript.

    Args:
        transcript: List of transcript segments

    Returns:
        list: List of timestamps with key points

    """
    # Configure Gemini API
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel(config.GEMINI_MODEL)

    # Combine transcript segments into a single text with timestamps
    full_text = ""
    for segment in transcript:
        minutes = int(segment["start"] // 60)
        seconds = int(segment["start"] % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
        full_text += f"[{timestamp}] {segment['text']}\n"

    # Create prompt for Gemini to identify key points
    prompt = f"""
    Below is a transcript of a YouTube video with timestamps.
    Please identify the most relevant key points or topics discussed in the video.
    If two or more timestamp segments are related, combine them into a single key point.
    For each key point, provide:
    1. The timestamp where the topic begins
    2. A brief title (3-7 words)
    3. A one-sentence summary of the point

    Format your answer as a list of timestamps with key points.

    Transcript:
    {full_text}
    """

    # Generate key points using Gemini
    response = model.generate_content(prompt)

    # Extract the text content from the Gemini response
    try:
        # Access the protobuf fields properly
        candidates = response._result.candidates
        if not candidates:
            logger.error("No candidates found in Gemini response")
            return []

        content_parts = candidates[0].content.parts
        if not content_parts:
            logger.error("No content parts found in Gemini response")
            return []

        response_text = content_parts[0].text

        # Parse timestamps with regex to handle the **[00:00]** format
        # This pattern looks for text with timestamps like **[00:00]**
        timestamp_pattern = re.compile(r'\*\*\[(\d+:\d+)\]\s*(.*?)\*\*')
        key_points = []

        for line in response_text.split('\n'):
            line = line.strip()
            match = timestamp_pattern.search(line)
            if match:
                timestamp = match.group(1)
                description = match.group(2)
                # Combine them with the original formatting or customize as needed
                key_point = f"[{timestamp}] {description}"
                key_points.append(key_point)
        return key_points

    except Exception as e:
        logger.exception("Failed to parse Gemini response: %s", e)
        return []
