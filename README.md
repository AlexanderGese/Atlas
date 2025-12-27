# Atlas - Personal AI Voice Assistant

A voice-activated AI assistant that responds to the wake word "Atlas", powered by OpenAI's Whisper and ChatGPT.

## Features

- Wake word detection ("Atlas")
- Speech-to-text using OpenAI Whisper
- Intelligent responses via ChatGPT
- Text-to-speech output

## Requirements

- Python 3.9+
- OpenAI API key
- Picovoice access key (for wake word detection)
- PortAudio (for audio input)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Atlas.git
cd Atlas
```

2. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio

# macOS
brew install portaudio
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
# Edit .env with your API keys
```

## Configuration

Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_openai_api_key_here
PICOVOICE_ACCESS_KEY=your_picovoice_access_key_here
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
│   ├── wake_word.py         # Wake word detection
│   ├── speech_to_text.py    # Whisper integration
│   ├── assistant.py         # ChatGPT integration
│   ├── text_to_speech.py    # TTS output
│   └── config.py            # Configuration
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT
