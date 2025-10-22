import reflex as rx
from app.state import UIState, Message


def user_message(message: Message) -> rx.Component:
    """A message from the user."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                message["content"],
                class_name=rx.cond(
                    UIState.theme == "light",
                    "text-base font-medium text-gray-800",
                    "text-base font-medium text-gray-100",
                ),
            ),
            class_name=rx.cond(
                UIState.theme == "light",
                "bg-gray-100 p-4 rounded-xl rounded-br-none shadow-sm border border-gray-200",
                "bg-gray-700 p-4 rounded-xl rounded-br-none shadow-sm border border-gray-600",
            ),
        ),
        class_name="flex justify-end w-full",
    )


def ai_message(message: Message) -> rx.Component:
    """A message from the AI assistant."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(message["content"], class_name="text-base font-medium text-white"),
            class_name="bg-blue-500 p-4 rounded-xl rounded-bl-none shadow-sm",
        ),
        class_name="flex justify-start w-full",
    )


def chat_header() -> rx.Component:
    """The header of the chat interface."""
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("bot", class_name="h-6 w-6 text-blue-500"),
                rx.el.h1(
                    "AI Chat",
                    class_name=rx.cond(
                        UIState.theme == "light",
                        "text-xl font-bold text-gray-800",
                        "text-xl font-bold text-gray-100",
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        UIState.theme == "light",
                        rx.icon("sun", class_name="h-4 w-4 text-gray-600"),
                        rx.icon("moon", class_name="h-4 w-4 text-gray-200"),
                    ),
                    on_click=UIState.toggle_theme,
                    class_name=rx.cond(
                        UIState.theme == "light",
                        "p-2 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 transition-colors",
                        "p-2 bg-gray-800 border border-gray-700 rounded-lg shadow-sm hover:bg-gray-700 transition-colors",
                    ),
                    aria_label="Toggle theme",
                ),
                rx.el.button(
                    rx.icon(
                        "trash-2",
                        class_name=rx.cond(
                            UIState.theme == "light",
                            "h-4 w-4 text-gray-600",
                            "h-4 w-4 text-gray-200",
                        ),
                    ),
                    on_click=UIState.clear_chat,
                    class_name=rx.cond(
                        UIState.theme == "light",
                        "p-2 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 transition-colors",
                        "p-2 bg-gray-800 border border-gray-700 rounded-lg shadow-sm hover:bg-gray-700 transition-colors",
                    ),
                    aria_label="Clear chat",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.el.div(
                            rx.el.span(
                                UIState.selected_model["name"],
                                class_name="font-semibold",
                            ),
                            rx.icon(
                                "chevrons-up-down",
                                class_name=rx.cond(
                                    UIState.show_model_selector,
                                    "h-4 w-4 text-gray-500 transform rotate-180 transition-transform",
                                    "h-4 w-4 text-gray-500 transition-transform",
                                ),
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        on_click=UIState.toggle_model_selector,
                        class_name=rx.cond(
                            UIState.theme == "light",
                            "flex items-center justify-between px-4 py-2 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 transition-colors text-gray-800",
                            "flex items-center justify-between px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg shadow-sm hover:bg-gray-700 transition-colors text-gray-100",
                        ),
                        aria_label="Select AI model",
                    ),
                    rx.cond(
                        UIState.show_model_selector,
                        rx.el.div(
                            rx.foreach(
                                UIState.models,
                                lambda model: rx.el.button(
                                    rx.el.div(
                                        rx.el.span(
                                            model["name"],
                                            class_name=rx.cond(
                                                UIState.theme == "light",
                                                "font-medium text-gray-700",
                                                "font-medium text-gray-200",
                                            ),
                                        ),
                                        rx.el.span(
                                            model["provider"],
                                            class_name="text-xs text-gray-500",
                                        ),
                                        class_name="flex flex-col items-start",
                                    ),
                                    on_click=lambda: UIState.select_model(model),
                                    class_name=rx.cond(
                                        UIState.theme == "light",
                                        "w-full text-left p-3 hover:bg-gray-100 rounded-md transition-colors",
                                        "w-full text-left p-3 hover:bg-gray-700 rounded-md transition-colors",
                                    ),
                                ),
                            ),
                            class_name=rx.cond(
                                UIState.theme == "light",
                                "absolute top-full right-0 mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-lg z-10 p-2",
                                "absolute top-full right-0 mt-2 w-56 bg-gray-800 border border-gray-700 rounded-lg shadow-lg z-10 p-2",
                            ),
                        ),
                        None,
                    ),
                    class_name="relative",
                ),
                class_name="flex items-center justify-between gap-4",
            ),
        ),
        class_name=rx.cond(
            UIState.theme == "light",
            "w-full max-w-4xl mx-auto p-4 bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10 shadow-sm",
            "w-full max-w-4xl mx-auto p-4 bg-gray-900/80 backdrop-blur-sm border-b border-gray-700 sticky top-0 z-10 shadow-sm",
        ),
    )


def thinking_indicator() -> rx.Component:
    """A thinking indicator for the AI assistant."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(class_name="w-2 h-2 bg-blue-500 rounded-full animate-pulse"),
                rx.el.span(
                    class_name="w-2 h-2 bg-blue-500 rounded-full animate-pulse",
                    style={"animation_delay": "0.2s"},
                ),
                rx.el.span(
                    class_name="w-2 h-2 bg-blue-500 rounded-full animate-pulse",
                    style={"animation_delay": "0.4s"},
                ),
                class_name="flex items-center gap-2",
            ),
            class_name=rx.cond(
                UIState.theme == "light",
                "bg-gray-100 p-4 rounded-xl rounded-bl-none shadow-sm border border-gray-200",
                "bg-gray-700 p-4 rounded-xl rounded-bl-none shadow-sm border border-gray-600",
            ),
        ),
        class_name="flex justify-start w-full",
    )


def chat_messages() -> rx.Component:
    """The area where chat messages are displayed."""
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                UIState.messages,
                lambda message: rx.cond(
                    message["role"] == "user",
                    user_message(message),
                    ai_message(message),
                ),
            ),
            rx.cond(UIState.is_loading, thinking_indicator(), None),
            rx.cond(
                (UIState.messages.length() == 0) & ~UIState.is_loading,
                rx.el.div(
                    rx.icon("message-circle", class_name="h-16 w-16 text-gray-400"),
                    rx.el.p(
                        "Start a conversation",
                        class_name=rx.cond(
                            UIState.theme == "light",
                            "text-gray-500 mt-4 font-medium",
                            "text-gray-400 mt-4 font-medium",
                        ),
                    ),
                    class_name="flex flex-col items-center justify-center h-full text-center",
                ),
                None,
            ),
            rx.el.div(id="end-of-chat", class_name="h-1"),
            class_name="flex flex-col gap-6 p-6 overflow-y-auto",
        ),
        class_name="flex-grow w-full max-w-4xl mx-auto",
    )


def chat_input() -> rx.Component:
    """The input field for sending messages."""
    return rx.el.div(
        rx.el.div(
            rx.el.form(
                rx.el.input(
                    placeholder="Type your message...",
                    name="prompt",
                    class_name=rx.cond(
                        UIState.theme == "light",
                        "w-full px-4 py-3 bg-transparent focus:outline-none text-gray-800 placeholder-gray-500 font-medium",
                        "w-full px-4 py-3 bg-transparent focus:outline-none text-gray-100 placeholder-gray-400 font-medium",
                    ),
                    aria_label="Chat input",
                ),
                rx.el.button(
                    rx.icon("arrow-up", class_name="h-5 w-5"),
                    type="submit",
                    class_name="bg-blue-500 text-white p-3 rounded-full hover:bg-blue-600 transition-colors shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed",
                    disabled=UIState.is_loading,
                    aria_label="Send message",
                ),
                on_submit=UIState.send_message,
                reset_on_submit=True,
                class_name=rx.cond(
                    UIState.theme == "light",
                    "flex items-center w-full bg-white border border-gray-200 rounded-full shadow-sm pr-2",
                    "flex items-center w-full bg-gray-800 border border-gray-700 rounded-full shadow-sm pr-2",
                ),
            ),
            class_name="w-full max-w-4xl mx-auto p-4",
        ),
        class_name=rx.cond(
            UIState.theme == "light",
            "bg-white/80 backdrop-blur-sm border-t border-gray-200 sticky bottom-0",
            "bg-gray-900/80 backdrop-blur-sm border-t border-gray-700 sticky bottom-0",
        ),
    )