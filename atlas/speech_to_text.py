"""Speech-to-text using OpenAI Whisper API."""

import io
import wave
import tempfile
import pyaudio
import numpy as np
from openai import OpenAI
from .config import Config


class SpeechToText:
    """Handles audio recording and transcription via Whisper."""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.audio = pyaudio.PyAudio()

    def record_audio(self) -> bytes:
        """
        Record audio until silence is detected.

        Returns:
            Audio data as bytes in WAV format.
        """
        stream = self.audio.open(
            rate=Config.SAMPLE_RATE,
            channels=Config.CHANNELS,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=Config.CHUNK_SIZE
        )

        print("Listening...")
        frames = []
        silent_chunks = 0
        chunks_per_second = Config.SAMPLE_RATE / Config.CHUNK_SIZE
        max_silent_chunks = int(Config.SILENCE_DURATION * chunks_per_second)
        max_chunks = int(Config.MAX_RECORDING_DURATION * chunks_per_second)

        for _ in range(max_chunks):
            data = stream.read(Config.CHUNK_SIZE, exception_on_overflow=False)
            frames.append(data)

            # Check for silence
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitude = np.abs(audio_data).mean()

            if amplitude < Config.SILENCE_THRESHOLD:
                silent_chunks += 1
                if silent_chunks >= max_silent_chunks and len(frames) > max_silent_chunks:
                    break
            else:
                silent_chunks = 0

        stream.stop_stream()
        stream.close()

        # Convert to WAV format
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wf:
            wf.setnchannels(Config.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(Config.SAMPLE_RATE)
            wf.writeframes(b"".join(frames))

        return wav_buffer.getvalue()

    def transcribe(self, audio_data: bytes) -> str:
        """
        Transcribe audio using Whisper API.

        Args:
            audio_data: Audio data in WAV format.

        Returns:
            Transcribed text.
        """
        # Write to temporary file (required by OpenAI API)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
            tmp.write(audio_data)
            tmp.flush()

            with open(tmp.name, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )

        return transcript.strip()

    def listen_and_transcribe(self) -> str:
        """Record audio and transcribe it."""
        audio_data = self.record_audio()
        return self.transcribe(audio_data)

    def cleanup(self) -> None:
        """Release resources."""
        self.audio.terminate()
