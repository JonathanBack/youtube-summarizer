"""Class for generating summaries using Gemini API."""
import logging

import config
import google.generativeai as genai

logger = logging.getLogger(__name__)

class SummaryGenerator:
    """Generates video summaries using the Gemini API."""

    def __init__(self):
        """Initialize the SummaryGenerator."""
        # Configure Gemini API
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)

    def generate(self, transcript, timestamps):
        """Generate a summary of a video transcript using Gemini.

        Args:
            transcript (list): List of transcript segments
            timestamps (list): List of key points with timestamps

        Returns:
            str: Generated summary

        """
        # Combine transcript segments into full text
        full_text = self._format_transcript(transcript)

        # Format key points
        key_points_text = "\n".join(timestamps)

        # Create prompt for summary generation
        prompt = self._create_prompt(full_text, key_points_text)

        # Generate summary
        response = self.model.generate_content(prompt)

        # Create formatted output with timestamps and summary
        return self._format_output(response.text, key_points_text)


    def _format_transcript(self, transcript):
        """Format transcript for the prompt."""
        full_text = ""
        for segment in transcript:
            full_text += segment["text"] + " "
        return full_text

    def _create_prompt(self, transcript_text, key_points_text):
        """Create the prompt for Gemini API."""
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
        {transcript_text[:15000]}  # Limit to first 15k characters
        """
        return prompt

    def _format_output(self, summary_text, key_points_text):
        """Format the final output."""
        formatted_summary = f"""
SUMMARY:
{summary_text}

KEY POINTS:
{key_points_text}
"""
        return formatted_summary