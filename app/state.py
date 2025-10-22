import reflex as rx
from typing import TypedDict, Literal, Union
import re


class ContentBlock(TypedDict):
    """A block of content, either text or code."""

    type: Literal["text", "code"]
    content: str
    language: str | None


class Message(TypedDict):
    """A chat message."""

    role: Literal["user", "assistant"]
    content: list[ContentBlock]


class Model(TypedDict):
    """An AI model."""

    name: str
    value: str
    provider: str


class UIState(rx.State):
    """Manages the UI state of the application."""

    theme: str = rx.LocalStorage("light", name="theme")
    messages: list[Message] = []
    show_model_selector: bool = False
    is_loading: bool = False
    models: list[Model] = [
        {"name": "GPT-4o", "value": "gpt-4o", "provider": "OpenAI"},
        {"name": "GPT-3.5 Turbo", "value": "gpt-3.5-turbo", "provider": "OpenAI"},
        {
            "name": "Qwen3 235B A22B (Free)",
            "value": "qwen/qwen3-235b-a22b:free",
            "provider": "OpenRouter",
        },
        {
            "name": "Gemini 2.5 Pro",
            "value": "models/gemini-2.5-pro",
            "provider": "Google",
        },
    ]
    selected_model: Model = models[3]

    @rx.event
    def toggle_theme(self):
        """Toggles the color theme."""
        self.theme = "dark" if self.theme == "light" else "light"

    @rx.event
    def toggle_model_selector(self):
        """Toggles the visibility of the model selector dropdown."""
        self.show_model_selector = not self.show_model_selector

    @rx.event
    def select_model(self, model: Model):
        """Selects an AI model and closes the dropdown."""
        self.selected_model = model
        self.show_model_selector = False

    @rx.event
    def clear_chat(self):
        """Clears the chat history."""
        self.messages = []
        self.is_loading = False

    @rx.event
    async def send_message(self, form_data: dict):
        """Adds the user's message and triggers the AI response."""
        from app.states.ai_state import AIState

        prompt = form_data.get("prompt", "").strip()
        if not prompt:
            return
        user_message_block: ContentBlock = {
            "type": "text",
            "content": prompt,
            "language": None,
        }
        self.messages.append({"role": "user", "content": [user_message_block]})
        self.is_loading = True
        yield
        yield AIState.get_response