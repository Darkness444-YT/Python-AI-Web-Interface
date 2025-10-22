import reflex as rx
from app.components.navbar import page_layout


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-8 w-8 text-blue-500"),
        rx.el.h3(title, class_name="mt-4 text-xl font-semibold"),
        rx.el.p(description, class_name="mt-2 text-gray-500 dark:text-gray-400"),
        class_name="rounded-lg border bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900",
    )


def about() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.h1("About AI Chat", class_name="text-4xl font-bold tracking-tight"),
            rx.el.p(
                "This application is a modern, responsive chat interface that allows you to interact with various powerful AI models.",
                class_name="mt-4 text-lg text-gray-500 dark:text-gray-400",
            ),
            rx.el.div(
                rx.el.h2(
                    "Features", class_name="text-3xl font-bold tracking-tight mt-12"
                ),
                rx.el.div(
                    feature_card(
                        "switch-camera",
                        "Model Switching",
                        "Seamlessly switch between different AI models from providers like OpenAI, Google, and OpenRouter.",
                    ),
                    feature_card(
                        "code",
                        "Code Block Rendering",
                        "Enjoy beautifully rendered code blocks with syntax highlighting and a one-click copy feature.",
                    ),
                    feature_card(
                        "moon",
                        "Light/Dark Mode",
                        "Toggle between light and dark themes for a comfortable viewing experience at any time of day.",
                    ),
                    feature_card(
                        "smartphone",
                        "Responsive Design",
                        "A fully responsive interface that works flawlessly on desktop, tablet, and mobile devices.",
                    ),
                    class_name="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2",
                ),
                class_name="mt-12",
            ),
        )
    )