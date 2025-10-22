import reflex as rx
import os
from openai import AsyncOpenAI
import google.generativeai as genai
from app.state import UIState
import logging


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
            history = [
                {"role": m["role"], "content": m["content"]} for m in ui_state.messages
            ]
        if provider == "OpenAI":
            async for _ in self._stream_openai(model, history):
                yield
        elif provider == "Google":
            async for _ in self._stream_google(model, history):
                yield

    async def _stream_openai(self, model: str, history: list[dict]):
        client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        async with self:
            ui_state = await self.get_state(UIState)
            ui_state.messages.append({"role": "assistant", "content": ""})
        try:
            stream = await client.chat.completions.create(
                model=model, messages=history, stream=True
            )
            async for chunk in stream:
                if content := chunk.choices[0].delta.content:
                    async with self:
                        ui_state = await self.get_state(UIState)
                        ui_state.messages[-1]["content"] += content
                    yield
        except Exception as e:
            logging.exception(f"OpenAI Error: {e}")
            async with self:
                ui_state = await self.get_state(UIState)
                ui_state.messages[-1]["content"] = (
                    f"Error: OpenAI API request failed. Please check your quota and API key. Details: {str(e)}"
                )
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
        async with self:
            ui_state = await self.get_state(UIState)
            ui_state.messages.append({"role": "assistant", "content": ""})
        try:
            chat_session = model_instance.start_chat(history=google_history)
            response = await chat_session.send_message_async(prompt, stream=True)
            async for chunk in response:
                if text_chunk := chunk.text:
                    async with self:
                        ui_state = await self.get_state(UIState)
                        ui_state.messages[-1]["content"] += text_chunk
                    yield
        except Exception as e:
            logging.exception(f"Google Gemini Error: {e}")
            async with self:
                ui_state = await self.get_state(UIState)
                ui_state.messages[-1]["content"] = (
                    f"Error: Google Gemini API request failed. Details: {str(e)}"
                )
        finally:
            async with self:
                ui_state = await self.get_state(UIState)
                ui_state.is_loading = False