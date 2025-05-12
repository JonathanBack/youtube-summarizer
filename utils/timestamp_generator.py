"""Module for generating timestamps with key points from transcripts."""
import logging

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
        minutes = int(segment["start_time"] // 60)
        seconds = int(segment["start_time"] % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
        full_text += f"[{timestamp}] {segment['text']}\n"

    # Create prompt for Gemini to identify key points
    prompt = f"""
    Below is a transcript of a YouTube video with timestamps. 
    Please identify 5-10 key points or topics discussed in the video. 
    For each key point, provide:
    1. The timestamp where the topic begins
    2. A brief title (3-7 words)
    3. A one-sentence summary of the point

    Format your answer as a list of timestamps with key points.

    Transcript:
    {full_text[:10000]}  # Limit to first 10k characters to stay within Gemini's context window
    """

    # Generate key points using Gemini
    response = model.generate_content(prompt)

    # Parse timestamps from the response
    # Note: This is a simple parsing approach; might need improvement for complex responses
    key_points = []
    for line_raw in response.text.split('\n'):
        line_stripped = line_raw.strip()
        if line_stripped and (':' in line_stripped[:5]):  # Simple check for timestamp format
            key_points.append(line_stripped)

    return key_points
