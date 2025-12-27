"""Text-to-speech output for Atlas."""

import pyttsx3
import threading


class TextToSpeech:
    """Handles text-to-speech output."""

    def __init__(self):
        self.engine = pyttsx3.init()
        self._configure_voice()
        self._lock = threading.Lock()

    def _configure_voice(self) -> None:
        """Configure TTS voice settings."""
        # Set speech rate (words per minute)
        self.engine.setProperty("rate", 175)

        # Set volume (0.0 to 1.0)
        self.engine.setProperty("volume", 1.0)

        # Try to use a natural-sounding voice
        voices = self.engine.getProperty("voices")
        for voice in voices:
            # Prefer female English voices for assistant personality
            if "english" in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                break

    def speak(self, text: str) -> None:
        """
        Speak the given text.

        Args:
            text: Text to speak.
        """
        with self._lock:
            self.engine.say(text)
            self.engine.runAndWait()

    def speak_async(self, text: str) -> None:
        """
        Speak the given text asynchronously.

        Args:
            text: Text to speak.
        """
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.start()

    def stop(self) -> None:
        """Stop any ongoing speech."""
        self.engine.stop()

    def cleanup(self) -> None:
        """Release resources."""
        self.engine.stop()
