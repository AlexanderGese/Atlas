"""Text-to-speech output using OpenAI TTS API."""

import os
import subprocess
import tempfile
import threading
from openai import OpenAI
from .config import Config


class TextToSpeech:
    """Handles text-to-speech output using OpenAI's TTS API."""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self._lock = threading.Lock()
        self._process = None
        # OpenAI TTS settings
        # Voices: alloy, echo, fable, onyx, nova, shimmer
        self.voice = "nova"  # Natural female voice
        self.model = "tts-1"  # Use "tts-1-hd" for higher quality

    def _find_player(self) -> list:
        """Find available audio player."""
        players = [
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"],
            ["mpv", "--no-video", "--really-quiet"],
            ["cvlc", "--play-and-exit", "--no-repeat", "--quiet"],
            ["vlc", "--intf", "dummy", "--play-and-exit", "--no-repeat", "--quiet"],
        ]
        for player in players:
            try:
                subprocess.run(["which", player[0]], capture_output=True, check=True)
                return player
            except subprocess.CalledProcessError:
                continue
        return None

    def speak(self, text: str) -> None:
        """
        Speak the given text using OpenAI TTS.

        Args:
            text: Text to speak.
        """
        with self._lock:
            try:
                # Generate speech with OpenAI
                response = self.client.audio.speech.create(
                    model=self.model,
                    voice=self.voice,
                    input=text,
                    response_format="mp3"
                )

                # Save to temp file
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                    tmp.write(response.content)
                    tmp_path = tmp.name

                # Find and use available player
                player = self._find_player()
                if player:
                    cmd = player + [tmp_path]
                    self._process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    self._process.wait()
                else:
                    print("Warning: No audio player found. Install ffmpeg, mpv, or vlc.")

                # Cleanup temp file
                os.unlink(tmp_path)

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
