import reflex as rx
from app.components.navbar import page_layout
from app.state import UIState


def index() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Welcome to AI Chat",
                    class_name="text-4xl md:text-5xl font-bold tracking-tight",
                ),
                rx.el.p(
                    "Your intelligent conversation partner, powered by the latest AI models.",
                    class_name="mt-4 text-lg text-gray-500 dark:text-gray-400",
                ),
                rx.el.a(
                    "Start Chatting",
                    href="/chat",
                    class_name="mt-8 inline-flex items-center justify-center rounded-md bg-blue-500 px-6 py-3 text-base font-medium text-white shadow-md transition-colors hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
                ),
                class_name="max-w-3xl text-center mx-auto",
            ),
            class_name="flex flex-col items-center justify-center py-12 md:py-24 lg:py-32",
        )
    )