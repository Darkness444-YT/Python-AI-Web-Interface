import reflex as rx
from app.components.navbar import page_layout
from app.state import UIState, Model


def model_selection_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Default AI Model", class_name="text-lg font-semibold"),
        rx.el.p(
            "Choose the default model for starting new conversations.",
            class_name="mt-1 text-sm text-gray-500 dark:text-gray-400",
        ),
        rx.el.select(
            rx.foreach(
                UIState.models,
                lambda model: rx.el.option(
                    f"{model['name']} ({model['provider']})", value=model["value"]
                ),
            ),
            value=UIState.selected_model["value"],
            on_change=UIState.select_model_by_value,
            class_name="mt-4 w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-800",
        ),
        class_name="rounded-lg border bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-950",
    )


def theme_selection_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Appearance", class_name="text-lg font-semibold"),
        rx.el.p(
            "Customize the look and feel of the application.",
            class_name="mt-1 text-sm text-gray-500 dark:text-gray-400",
        ),
        rx.el.div(
            rx.el.p("Interface Theme", class_name="font-medium"),
            rx.el.div(
                rx.el.button(
                    rx.icon("sun", class_name="mr-2"),
                    "Light",
                    on_click=UIState.set_theme("light"),
                    class_name=rx.cond(
                        UIState.theme == "light",
                        "flex items-center justify-center rounded-l-lg border bg-gray-100 px-4 py-2 text-sm font-medium dark:bg-gray-700",
                        "flex items-center justify-center rounded-l-lg border bg-white px-4 py-2 text-sm font-medium hover:bg-gray-50 dark:border-gray-800 dark:bg-gray-950 dark:hover:bg-gray-800",
                    ),
                ),
                rx.el.button(
                    rx.icon("moon", class_name="mr-2"),
                    "Dark",
                    on_click=UIState.set_theme("dark"),
                    class_name=rx.cond(
                        UIState.theme == "dark",
                        "flex items-center justify-center rounded-r-lg border bg-gray-100 px-4 py-2 text-sm font-medium dark:bg-gray-700",
                        "flex items-center justify-center rounded-r-lg border bg-white px-4 py-2 text-sm font-medium hover:bg-gray-50 dark:border-gray-800 dark:bg-gray-950 dark:hover:bg-gray-800",
                    ),
                ),
                class_name="isolate inline-flex rounded-md shadow-sm mt-4",
            ),
            class_name="mt-4 flex items-center justify-between",
        ),
        class_name="rounded-lg border bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-950",
    )


def settings() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.h1("Settings", class_name="text-4xl font-bold tracking-tight"),
            rx.el.div(
                model_selection_card(),
                theme_selection_card(),
                class_name="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2",
            ),
        )
    )