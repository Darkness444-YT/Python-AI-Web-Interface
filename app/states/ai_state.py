import reflex as rx
import os
from openai import AsyncOpenAI
import google.generativeai as genai
from app.state import UIState
import logging
import re


class AIState(rx.State):
    """Manages the AI model interactions."""

    @rx.event(background=True)
    async def get_response(self):
        async with self:
            ui_state = await self.get_state(UIState)
            if not ui_state.messages:
                ui_state.is_loading = False
                return
            provider = ui_state.selected_model["provider"]
            model = ui_state.selected_model["value"]
            history = []
            for m in ui_state.messages:
                content = " ".join(
                    [
                        block["content"]
                        for block in m["content"]
                        if block["type"] == "text"
                    ]
                )
                history.append({"role": m["role"], "content": content})
        if provider == "OpenAI":
            async for _ in self._stream_openai(model, history):
                yield
        elif provider == "Google":
            async for _ in self._stream_google(model, history):
                yield
        elif provider == "OpenRouter":
            async for _ in self._stream_openrouter(model, history):
                yield

    def _parse_and_update_content(self, full_content: str, ui_state: UIState):
        """Parses content for code blocks and updates the message state."""
        new_content_blocks = []
        last_end = 0
        backtick = chr(96)
        pattern = f"{backtick * 3}([a-zA-Z0-9]*)\\n(.*?)\\n{backtick * 3}"
        for match in re.finditer(pattern, full_content, re.DOTALL):
            text_part = full_content[last_end : match.start()].strip()
            if text_part:
                new_content_blocks.append(
                    {"type": "text", "content": text_part, "language": None}
                )
            language = match.group(1) or "plaintext"
            code_part = match.group(2).strip()
            new_content_blocks.append(
                {"type": "code", "content": code_part, "language": language}
            )
            last_end = match.end()
        remaining_text = full_content[last_end:].strip()
        if remaining_text:
            new_content_blocks.append(
                {"type": "text", "content": remaining_text, "language": None}
            )
        if not new_content_blocks and full_content.strip():
            new_content_blocks.append(
                {"type": "text", "content": full_content.strip(), "language": None}
            )
        if new_content_blocks:
            ui_state.messages[-1]["content"] = new_content_blocks

    async def _stream_openai(self, model: str, history: list[dict]):
        client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        full_response = ""
        async with self:
            ui_state = await self.get_state(UIState)
            ui_state.messages.append(
                {
                    "role": "assistant",
                    "content": [{"type": "text", "content": "", "language": None}],
                }
            )
        try:
            stream = await client.chat.completions.create(
                model=model, messages=history, stream=True
            )
            async for chunk in stream:
                if content := chunk.choices[0].delta.content:
                    full_response += content
                    async with self:
                        ui_state = await self.get_state(UIState)
                        self._parse_and_update_content(full_response, ui_state)
                    yield
        except Exception as e:
            logging.exception(f"OpenAI Error: {e}")
            async with self:
                ui_state = await self.get_state(UIState)
                error_message = f"Error: OpenAI API request failed. Please check your quota and API key. Details: {str(e)}"
                ui_state.messages[-1]["content"] = [
                    {"type": "text", "content": error_message, "language": None}
                ]
        finally:
            async with self:
                ui_state = await self.get_state(UIState)
                ui_state.is_loading = False

    async def _stream_openrouter(self, model: str, history: list[dict]):
        client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            default_headers={"HTTP-Referer": "http://localhost:3000"},
        )
        full_response = ""
        async with self:
            ui_state = await self.get_state(UIState)
            ui_state.messages.append(
                {
                    "role": "assistant",
                    "content": [{"type": "text", "content": "", "language": None}],
                }
            )
        try:
            stream = await client.chat.completions.create(
                model=model, messages=history, stream=True
            )
            async for chunk in stream:
                if content := chunk.choices[0].delta.content:
                    full_response += content
                    async with self:
                        ui_state = await self.get_state(UIState)
                        self._parse_and_update_content(full_response, ui_state)
                    yield
        except Exception as e:
            logging.exception(f"OpenRouter Error: {e}")
            async with self:
                ui_state = await self.get_state(UIState)
                error_message = f"Error: OpenRouter API request failed. Please check your API key and that the model is available. Details: {str(e)}"
                ui_state.messages[-1]["content"] = [
                    {"type": "text", "content": error_message, "language": None}
                ]
        finally:
            async with self:
                ui_state = await self.get_state(UIState)
                ui_state.is_loading = False

    async def _stream_google(self, model: str, history: list[dict]):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        model_instance = genai.GenerativeModel(model)
        google_history = []
        for msg in history[:-1]:
            google_history.append(
                {
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [{"text": msg["content"]}],
                }
            )
        prompt = history[-1]["content"]
        full_response = ""
        async with self:
            ui_state = await self.get_state(UIState)
            ui_state.messages.append(
                {
                    "role": "assistant",
                    "content": [{"type": "text", "content": "", "language": None}],
                }
            )
        try:
            chat_session = model_instance.start_chat(history=google_history)
            response = await chat_session.send_message_async(prompt, stream=True)
            async for chunk in response:
                if text_chunk := chunk.text:
                    full_response += text_chunk
                    async with self:
                        ui_state = await self.get_state(UIState)
                        self._parse_and_update_content(full_response, ui_state)
                    yield
        except Exception as e:
            logging.exception(f"Google Gemini Error: {e}")
            async with self:
                ui_state = await self.get_state(UIState)
                error_message = (
                    f"Error: Google Gemini API request failed. Details: {str(e)}"
                )
                ui_state.messages[-1]["content"] = [
                    {"type": "text", "content": error_message, "language": None}
                ]
        finally:
            async with self:
                ui_state = await self.get_state(UIState)
                ui_state.is_loading = False