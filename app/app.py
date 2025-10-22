import reflex as rx
from app.components.chat import chat_header, chat_messages, chat_input
from app.state import UIState
from app.states.ai_state import AIState


def index() -> rx.Component:
    """The main chat interface page."""
    return rx.el.main(
        rx.el.div(
            chat_header(),
            chat_messages(),
            chat_input(),
            class_name="flex flex-col h-screen",
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


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="blue"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)