# YouTube Video Summarizer

A Python tool to automatically generate summaries of YouTube videos using AI.

## Features

- Fetch video transcripts using the YouTube API
- Download videos and transcribe them using OpenAI's Whisper when transcripts aren't available
- Generate key timestamps for important points in the video
- Create concise AI-powered summaries using Google's Gemini API

## Project Structure

```
youtube-summarizer/
├── processors/         # Core processing classes
├── transcribers/       # Transcript acquisition classes
├── utils/              # Helper utilities
└── tests/              # Unit tests
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-summarizer.git
cd youtube-summarizer
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
YOUTUBE_API_KEY=your_youtube_api_key
GEMINI_API_KEY=your_gemini_api_key
WHISPER_MODEL=base
```

## Usage

Run the script with the YouTube video URL:

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --method api
```

Options:
- `--method`: Choose between `api` (YouTube API) or `download` (youtube-dl + Whisper)
- `--force-download`: Force download and transcription even if API transcription is available

## Requirements

- Python 3.8+
- youtube-dl
- google-api-python-client
- openai-whisper
- google-generativeai

## License

[MIT License](LICENSE)
