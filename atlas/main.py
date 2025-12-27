"""Main entry point for Atlas voice assistant."""

import sys
import signal
from .config import Config
from .wake_word import create_detector
from .speech_to_text import SpeechToText
from .assistant import Assistant
from .text_to_speech import TextToSpeech


class Atlas:
    """Main Atlas voice assistant class."""

    def __init__(self):
        self.running = False
        self.wake_word_detector = None
        self.stt = None
        self.assistant = None
        self.tts = None

    def initialize(self) -> bool:
        """Initialize all components."""
        # Validate configuration
        errors = Config.validate()
        if errors:
            for error in errors:
                print(f"Configuration error: {error}")
            return False

        print("Initializing Atlas...")

        try:
            print("  - Setting up wake word detection...")
            self.wake_word_detector = create_detector()

            print("  - Setting up speech-to-text...")
            self.stt = SpeechToText()

            print("  - Setting up ChatGPT assistant...")
            self.assistant = Assistant()

            print("  - Setting up text-to-speech...")
            self.tts = TextToSpeech()

            print("Atlas initialized successfully!")
            return True

        except Exception as e:
            print(f"Failed to initialize: {e}")
            self.cleanup()
            return False

    def run(self) -> None:
        """Main loop - listen for wake word and process commands."""
        self.running = True
        print("\nAtlas is listening. Say 'Atlas' to wake me up...")
        print("Press Ctrl+C to exit.\n")

        # Announce ready
        self.tts.speak("Atlas is ready.")

        while self.running:
            try:
                # Listen for wake word
                if self.wake_word_detector.listen_for_wake_word():
                    self._handle_command()

            except KeyboardInterrupt:
                print("\nShutting down...")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

    def _handle_command(self) -> None:
        """Handle a voice command after wake word detection."""
        # Acknowledge wake word
        print("\n[Wake word detected!]")
        self.tts.speak("Yes?")

        # Listen and transcribe
        try:
            user_input = self.stt.listen_and_transcribe()
            if not user_input or user_input.strip() == "":
                self.tts.speak("I didn't catch that.")
                return

            print(f"You: {user_input}")

            # Get response from ChatGPT
            response = self.assistant.get_response(user_input)
            print(f"Atlas: {response}")

            # Speak the response
            self.tts.speak(response)

        except Exception as e:
            print(f"Error processing command: {e}")
            self.tts.speak("Sorry, I encountered an error.")

    def cleanup(self) -> None:
        """Clean up resources."""
        self.running = False
        if self.wake_word_detector:
            self.wake_word_detector.cleanup()
        if self.stt:
            self.stt.cleanup()
        if self.tts:
            self.tts.cleanup()


def main():
    """Entry point."""
    atlas = Atlas()

    # Handle signals gracefully
    def signal_handler(sig, frame):
        print("\nReceived shutdown signal...")
        atlas.cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize and run
    if atlas.initialize():
        try:
            atlas.run()
        finally:
            atlas.cleanup()
    else:
        print("Failed to initialize Atlas. Please check your configuration.")
        sys.exit(1)


if __name__ == "__main__":
    main()
