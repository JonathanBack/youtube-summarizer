# YouTube Video Summarizer

A Python tool to automatically generate summaries of YouTube videos using AI.

## Features

- Fetch video transcripts using `youtube-transcript-api`
- Download videos and transcribe them using OpenAI's Whisper when transcripts aren't available
- Generate key timestamps for important points in the video
- Create concise AI-powered summaries using Google's Gemini API

## Project Structure

```
youtube-summarizer/ 
├── utils/ # Helper utilities 
├── main.py # Entry point for the application 
├── config.py # Configuration settings 
├── requirements.txt # Project dependencies 
└── README.md # Documentation
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

3. Install ffmpeg (required for Whisper):

On Linux:
```bash
sudo apt-get install ffmpeg
```

Or via Python:
```bash
pip install imageio[ffmpeg]
```

4. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
WHISPER_MODEL=base
OUTPUT_DIR=output
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
- pytube
- youtube-transcript-api
- openai-whisper
- tqdm
- google-generativeai
- ffmpeg

## License

[MIT License](LICENSE)
