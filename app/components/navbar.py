import reflex as rx
from app.state import UIState


def nav_link(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        class_name=rx.cond(
            UIState.current_page == href.strip("/"),
            rx.cond(
                UIState.theme == "light",
                "px-4 py-2 text-sm font-semibold text-blue-600 bg-blue-50 rounded-lg",
                "px-4 py-2 text-sm font-semibold text-blue-400 bg-gray-700 rounded-lg",
            ),
            rx.cond(
                UIState.theme == "light",
                "px-4 py-2 text-sm font-semibold text-gray-600 hover:text-blue-600 hover:bg-gray-100 rounded-lg transition-colors",
                "px-4 py-2 text-sm font-semibold text-gray-300 hover:text-blue-400 hover:bg-gray-700 rounded-lg transition-colors",
            ),
        ),
        on_click=UIState.set_mobile_menu_open(False),
    )


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("bot", class_name="h-6 w-6 text-blue-500"),
                    href="/",
                    class_name="flex items-center gap-2",
                ),
                rx.el.nav(
                    nav_link("Home", "/"),
                    nav_link("Chat", "/chat"),
                    nav_link("About", "/about"),
                    nav_link("Settings", "/settings"),
                    class_name="hidden md:flex items-center gap-2",
                ),
                class_name="flex items-center gap-6",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        UIState.theme == "light",
                        rx.icon("sun", class_name="h-5 w-5 text-gray-600"),
                        rx.icon("moon", class_name="h-5 w-5 text-gray-200"),
                    ),
                    on_click=UIState.toggle_theme,
                    class_name=rx.cond(
                        UIState.theme == "light",
                        "p-2 rounded-lg hover:bg-gray-100 transition-colors",
                        "p-2 rounded-lg hover:bg-gray-700 transition-colors",
                    ),
                    aria_label="Toggle theme",
                ),
                rx.el.button(
                    rx.icon("menu", class_name="h-6 w-6"),
                    on_click=UIState.toggle_mobile_menu,
                    class_name="md:hidden",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="container mx-auto flex items-center justify-between p-4",
        ),
        rx.cond(
            UIState.mobile_menu_open,
            rx.el.div(
                rx.el.nav(
                    nav_link("Home", "/"),
                    nav_link("Chat", "/chat"),
                    nav_link("About", "/about"),
                    nav_link("Settings", "/settings"),
                    class_name="flex flex-col gap-4 p-4",
                ),
                class_name="md:hidden",
            ),
        ),
        class_name=rx.cond(
            UIState.theme == "light",
            "sticky top-0 z-20 w-full border-b border-gray-200 bg-white/80 backdrop-blur-lg",
            "sticky top-0 z-20 w-full border-b border-gray-800 bg-gray-900/80 backdrop-blur-lg",
        ),
    )


def page_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(content, class_name="container mx-auto p-4 md:p-6 lg:p-8"),
        class_name=rx.cond(
            UIState.theme == "light",
            "font-['Inter'] bg-gray-50 min-h-screen",
            "font-['Inter'] bg-gray-950 min-h-screen text-gray-100",
        ),
    )