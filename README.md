# Atlas - Personal AI Voice Assistant

A voice-activated AI assistant that responds to the wake word "Atlas", powered by OpenAI's Whisper and ChatGPT.

## Features

- Wake word detection (free, using Vosk - fully offline)
- Speech-to-text using OpenAI Whisper
- Intelligent responses via ChatGPT
- Text-to-speech output

## Requirements

- Python 3.9+ (tested on Python 3.13)
- OpenAI API key (only paid service required)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AlexanderGese/Atlas.git
cd Atlas
```

2. Install system dependencies (for TTS):
```bash
# Ubuntu/Debian
sudo apt-get install espeak-ng

# macOS
brew install espeak
```

3. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Configuration

Create a `.env` file with your API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

```bash
python -m atlas.main
```

Say "Atlas" to wake up the assistant, then speak your query.

## Project Structure

```
Atlas/
├── atlas/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── wake_word.py         # Wake word detection (Vosk - free, offline)
│   ├── speech_to_text.py    # Whisper integration
│   ├── assistant.py         # ChatGPT integration
│   ├── text_to_speech.py    # TTS output
│   └── config.py            # Configuration
├── requirements.txt
├── .env.example
└── README.md
```

## Cost

The only cost is the OpenAI API usage:
- **Whisper**: ~$0.006 per minute of audio
- **GPT-4o-mini**: ~$0.15 per 1M input tokens, $0.60 per 1M output tokens

Wake word detection is completely free using Vosk (runs offline, no API needed).

## License

MIT
