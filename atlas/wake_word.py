"""Wake word detection using Vosk (free & offline)."""

import json
import numpy as np
import sounddevice as sd
from scipy import signal
from vosk import Model, KaldiRecognizer
from .config import Config


class WakeWordDetector:
    """Detects the wake word 'Atlas' using Vosk (free, offline speech recognition)."""

    def __init__(self):
        self.model = None
        self.recognizer = None
        self.stream = None
        self.resample_ratio = Config.DEVICE_SAMPLE_RATE / Config.VOSK_SAMPLE_RATE

    def initialize(self) -> None:
        """Initialize Vosk and audio stream."""
        # Load Vosk model - will auto-download small English model
        print("  - Loading Vosk model (first run may download ~50MB)...")
        self.model = Model(lang="en-us")
        self.recognizer = KaldiRecognizer(self.model, Config.VOSK_SAMPLE_RATE)
        self.recognizer.SetWords(True)

        # Open audio input stream at device's native sample rate
        self.stream = sd.InputStream(
            samplerate=Config.DEVICE_SAMPLE_RATE,
            channels=Config.CHANNELS,
            dtype=np.int16,
            blocksize=Config.CHUNK_SIZE
        )
        self.stream.start()

    def _resample(self, audio: np.ndarray) -> np.ndarray:
        """Resample audio from device rate to Vosk rate (16kHz)."""
        if self.resample_ratio == 1.0:
            return audio

        # Calculate new length
        new_length = int(len(audio) / self.resample_ratio)
        # Resample using scipy
        resampled = signal.resample(audio.flatten(), new_length)
        return resampled.astype(np.int16)

    def listen_for_wake_word(self) -> bool:
        """
        Listen for the wake word "Atlas".

        Returns:
            True when wake word is detected.
        """
        if not self.recognizer or not self.stream:
            raise RuntimeError("Wake word detector not initialized")

        # Read audio chunk at device sample rate
        data, overflowed = self.stream.read(Config.CHUNK_SIZE)

        # Resample to 16kHz for Vosk
        resampled = self._resample(data)
        audio_bytes = resampled.tobytes()

        # Process with Vosk
        if self.recognizer.AcceptWaveform(audio_bytes):
            result = json.loads(self.recognizer.Result())
            text = result.get("text", "").lower()

            # Check for wake word
            if "atlas" in text:
                # Reset recognizer for next detection
                self.recognizer.Reset()
                return True

        # Also check partial results for faster response
        partial = json.loads(self.recognizer.PartialResult())
        partial_text = partial.get("partial", "").lower()

        if "atlas" in partial_text:
            self.recognizer.Reset()
            return True

        return False

    def cleanup(self) -> None:
        """Release resources."""
        if self.stream:
            self.stream.stop()
            self.stream.close()


def create_detector() -> WakeWordDetector:
    """Factory function to create and initialize a wake word detector."""
    detector = WakeWordDetector()
    detector.initialize()
    return detector
