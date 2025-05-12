"""Module for transcribing audio using OpenAI's Whisper model."""

import json
import logging
from pathlib import Path

import whisper

import config

logger = logging.getLogger(__name__)

def transcribe_audio(audio_file: str) -> list:
    """Transcribe an audio file using Whisper.

    Args:
        audio_file: Path to the audio file

    Returns:
        list: Transcript data with timestamps

    """
    # Generate transcript output path
    audio_path = Path(audio_file)
    transcript_path = audio_path.parent / f"{audio_path.stem}_transcript.json"

    # Skip transcription if transcript file already exists
    if transcript_path.exists():
        logger.info("Loading existing transcript: %s", transcript_path)
        with transcript_path.open('r', encoding='utf-8') as f:
            return json.load(f)

    # Load Whisper model
    logger.info("Loading Whisper model: %s", config.WHISPER_MODEL)
    model = whisper.load_model(config.WHISPER_MODEL)

    # Transcribe audio
    logger.info("Transcribing audio with Whisper...")
    result = model.transcribe(
        audio_file,
        fp16=False,  # Use True if you have GPU with FP16 support
        verbose=True,
    )

    # Format transcript
    transcript = [{
        "start_time": segment["start"],
        "end_time": segment["end"],
        "text": segment["text"].strip(),
    } for segment in result["segments"]]

    # Save transcript to file
    with transcript_path.open('w', encoding='utf-8') as f:
        json.dump(transcript, f, indent=2, ensure_ascii=False)

    logger.info("Transcript saved to: %s", transcript_path)
    return transcript
