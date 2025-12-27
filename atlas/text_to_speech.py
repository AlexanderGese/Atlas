"""Text-to-speech output for Atlas using espeak-ng."""

import subprocess
import threading


class TextToSpeech:
    """Handles text-to-speech output using espeak-ng."""

    def __init__(self):
        self._lock = threading.Lock()
        self._process = None
        # espeak-ng settings
        self.speed = 175  # words per minute
        self.voice = "en"  # English voice

    def speak(self, text: str) -> None:
        """
        Speak the given text.

        Args:
            text: Text to speak.
        """
        with self._lock:
            try:
                self._process = subprocess.Popen(
                    ["espeak-ng", "-v", self.voice, "-s", str(self.speed), text],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self._process.wait()
            except FileNotFoundError:
                print("Warning: espeak-ng not found. TTS disabled.")
            except Exception as e:
                print(f"TTS error: {e}")

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
        if self._process:
            self._process.terminate()

    def cleanup(self) -> None:
        """Release resources."""
        self.stop()
