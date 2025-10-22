import reflex as rx
from app.components.chat import chat_header, chat_messages, chat_input
from app.state import UIState


def chat() -> rx.Component:
    """The main chat interface page."""
    return rx.el.main(
        rx.el.div(
            chat_header(),
            chat_messages(),
            chat_input(),
            class_name="flex flex-col h-[calc(100vh-80px)]",
        ),
        rx.window_event_listener(
            on_key_down=lambda key: rx.cond(
                key == "Escape",
                rx.cond(
                    UIState.show_model_selector,
                    UIState.toggle_model_selector,
                    rx.noop(),
                ),
                rx.noop(),
            )
        ),
        rx.fragment(
            rx.el.script("""
                const endOfChat = document.getElementById('end-of-chat');
                if (endOfChat) {
                    endOfChat.scrollIntoView({ behavior: 'smooth' });
                }
                """)
        ),
        class_name=rx.cond(
            UIState.theme == "light",
            "font-['Inter'] bg-gray-50",
            "font-['Inter'] bg-gray-900",
        ),
    )