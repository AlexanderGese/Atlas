"""Configuration management for Atlas."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Config:
    """Configuration settings for Atlas."""

    # OpenAI API key for Whisper and ChatGPT
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Wake word sensitivity (0.0 to 1.0, higher = more strict)
    WAKE_WORD_SENSITIVITY: float = float(os.getenv("WAKE_WORD_SENSITIVITY", "0.5"))

    # Audio settings
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    CHUNK_SIZE: int = 512

    # Recording settings
    SILENCE_THRESHOLD: int = int(os.getenv("SILENCE_THRESHOLD", "500"))
    SILENCE_DURATION: float = float(os.getenv("SILENCE_DURATION", "1.5"))
    MAX_RECORDING_DURATION: float = float(os.getenv("MAX_RECORDING_DURATION", "30.0"))

    # ChatGPT settings
    GPT_MODEL: str = os.getenv("GPT_MODEL", "gpt-4o-mini")
    SYSTEM_PROMPT: str = os.getenv(
        "SYSTEM_PROMPT",
        "You are Atlas, a helpful voice assistant. Keep responses concise and conversational."
    )

    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration values."""
        errors = []
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is not set")
        return errors
