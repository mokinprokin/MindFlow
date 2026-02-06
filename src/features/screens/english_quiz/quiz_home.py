import flet as ft
import asyncio
from .view import QuizView
from .services.window import WindowService
from .utils import handle_key_event


async def main(page: ft.Page):
    WindowService.apply_settings(page)

    quiz = QuizView(page)
    layout = await quiz.main_layout()
    page.on_keyboard_event = lambda e: asyncio.create_task(handle_key_event(page, e))
    page.add(layout)
    page.update()


if __name__ == "__main__":
    ft.run(main=main)
