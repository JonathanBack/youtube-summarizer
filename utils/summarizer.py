"""Module for generating summaries using Gemini API."""
import logging

import google.generativeai as genai

import config

logger = logging.getLogger(__name__)

def generate_summary(transcript: list, timestamps: list) -> str:
    """Generate a summary of a video transcript using Gemini.

    Args:
        transcript: List of transcript segments
        timestamps: List of key points with timestamps

    Returns:
        str: Generated summary

    """
    # Configure Gemini API
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel(config.GEMINI_MODEL)

    # Combine transcript segments into full text
    full_text = ""
    for segment in transcript:
        full_text += segment["text"] + " "

    # Format key points
    key_points_text = "\n".join(timestamps)

    # Create prompt for summary generation
    prompt = f"""
    Please create a comprehensive summary of the following video transcript.
    The summary should:
    1. Start with a brief overview of the video's main topic (1-2 sentences)
    2. Include the main ideas and key insights
    3. Maintain the original meaning and context
    4. Be well-structured and readable
    5. Be around 3-5 paragraphs in length

    Here are the key points identified in the video:
    {key_points_text}

    Here's the transcript to summarize:
    {full_text}
    """

    # Generate summary
    response = model.generate_content(prompt)

    # Create formatted output with timestamps and summary
    formatted_summary = f"""
SUMMARY:
{response.text}

KEY POINTS:
{key_points_text}
"""

    return formatted_summary
