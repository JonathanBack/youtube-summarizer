"""Class for generating timestamps with key points from transcripts."""

import logging

import config
import google.generativeai as genai

logger = logging.getLogger(__name__)


class TimestampGenerator:
    """Generates timestamps with key points from transcripts using Gemini API."""

    def __init__(self):
        """Initialize the TimestampGenerator."""
        # Configure Gemini API
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)

    def generate(self, transcript):
        """Generate timestamps with key points from a transcript.

        Args:
            transcript (list): List of transcript segments

        Returns:
            list: List of timestamps with key points

        """
        # Combine transcript segments into a single text with timestamps
        full_text = self._format_transcript_for_prompt(transcript)

        # Create prompt for Gemini to identify key points
        prompt = self._create_prompt(full_text)

        # Generate key points using Gemini
        response = self.model.generate_content(prompt)

        # Parse timestamps from the response
        key_points = self._parse_response(response.text)

        return key_points

    def _format_transcript_for_prompt(self, transcript):
        """Format transcript for the prompt."""
        full_text = ""
        for segment in transcript:
            minutes = int(segment["start_time"] // 60)
            seconds = int(segment["start_time"] % 60)
            timestamp = f"{minutes:02d}:{seconds:02d}"
            full_text += f"[{timestamp}] {segment['text']}\n"

        return full_text

    def _create_prompt(self, transcript_text):
        """Create the prompt for Gemini API."""
        prompt = f"""
        Below is a transcript of a YouTube video with timestamps. 
        Please identify 5-10 key points or topics discussed in the video. 
        For each key point, provide:
        1. The timestamp where the topic begins
        2. A brief title (3-7 words)
        3. A one-sentence summary of the point

        Format your answer as a list of timestamps with key points.

        Transcript:
        {transcript_text[:10000]}  # Limit to first 10k characters to stay within Gemini's context window
        """
        return prompt

    def _parse_response(self, response_text):
        """Parse the Gemini API response to extract key points."""
        key_points = []
        for line in response_text.split("\n"):
            line = line.strip()
            if line and (":" in line[:5]):  # Simple check for timestamp format
                key_points.append(line)

        return key_points
