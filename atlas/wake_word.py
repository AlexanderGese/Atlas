"""Wake word detection using OpenWakeWord (free & open-source)."""

import numpy as np
import pyaudio
from openwakeword.model import Model
from .config import Config


class WakeWordDetector:
    """Detects the wake word 'Alexa' using OpenWakeWord (free alternative)."""

    def __init__(self):
        self.model = None
        self.audio = None
        self.stream = None
        self.frame_length = 1280  # OpenWakeWord expects 80ms chunks at 16kHz

    def initialize(self) -> None:
        """Initialize OpenWakeWord and audio stream."""
        # Load OpenWakeWord model - using "alexa" as it's a pre-trained model
        # The model responds to "Alexa" but you say "Atlas" (sounds similar enough!)
        # For a custom wake word, you can train your own model
        self.model = Model(
            wakeword_models=["alexa"],  # Pre-trained model included with openwakeword
            inference_framework="onnx"
        )

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            rate=Config.SAMPLE_RATE,
            channels=Config.CHANNELS,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.frame_length
        )

    def listen_for_wake_word(self) -> bool:
        """
        Listen for the wake word.

        Returns:
            True when wake word is detected.
        """
        if not self.model or not self.stream:
            raise RuntimeError("Wake word detector not initialized")

        # Read audio chunk
        audio_data = self.stream.read(self.frame_length, exception_on_overflow=False)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # Process with OpenWakeWord
        prediction = self.model.predict(audio_array)

        # Check if any wake word was detected (threshold-based)
        for model_name, score in prediction.items():
            if score > Config.WAKE_WORD_SENSITIVITY:
                # Reset the model state after detection
                self.model.reset()
                return True

        return False

    def cleanup(self) -> None:
        """Release resources."""
        if self.stream:
            self.stream.close()
        if self.audio:
            self.audio.terminate()


def create_detector() -> WakeWordDetector:
    """Factory function to create and initialize a wake word detector."""
    detector = WakeWordDetector()
    detector.initialize()
    return detector
