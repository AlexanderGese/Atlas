"""ChatGPT integration for Atlas."""

from openai import OpenAI
from .config import Config


class Assistant:
    """Handles conversation with ChatGPT."""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.conversation_history: list[dict] = []
        self.max_history = 10  # Keep last N exchanges

    def get_response(self, user_input: str) -> str:
        """
        Get a response from ChatGPT.

        Args:
            user_input: The user's transcribed speech.

        Returns:
            ChatGPT's response.
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Trim history if too long
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]

        # Build messages with system prompt
        messages = [
            {"role": "system", "content": Config.SYSTEM_PROMPT}
        ] + self.conversation_history

        # Get response from ChatGPT
        response = self.client.chat.completions.create(
            model=Config.GPT_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        assistant_message = response.choices[0].message.content

        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
