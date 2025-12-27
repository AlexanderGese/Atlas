"""Wake word detection using Porcupine."""

import struct
import pyaudio
import pvporcupine
from .config import Config


class WakeWordDetector:
    """Detects the wake word 'Atlas' using Picovoice Porcupine."""

    def __init__(self):
        self.porcupine = None
        self.audio = None
        self.stream = None

    def initialize(self) -> None:
        """Initialize Porcupine and audio stream."""
        # Create Porcupine instance with built-in "Alexa" keyword
        # Note: For custom "Atlas" wake word, you'll need to train one at Picovoice Console
        self.porcupine = pvporcupine.create(
            access_key=Config.PICOVOICE_ACCESS_KEY,
            keywords=["alexa"],  # Using "alexa" as placeholder; replace with custom "atlas" keyword
            sensitivities=[Config.WAKE_WORD_SENSITIVITY]
        )

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def listen_for_wake_word(self) -> bool:
        """
        Listen for the wake word.

        Returns:
            True when wake word is detected.
        """
        if not self.porcupine or not self.stream:
            raise RuntimeError("Wake word detector not initialized")

        pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

        keyword_index = self.porcupine.process(pcm)
        return keyword_index >= 0

    def cleanup(self) -> None:
        """Release resources."""
        if self.stream:
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        if self.porcupine:
            self.porcupine.delete()


def create_detector() -> WakeWordDetector:
    """Factory function to create and initialize a wake word detector."""
    detector = WakeWordDetector()
    detector.initialize()
    return detector
