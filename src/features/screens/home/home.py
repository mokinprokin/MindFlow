import flet as ft


async def main(page: ft.Page):
    from .services.window import WindowService

    WindowService.apply_settings(page)
    page.update()

    from src.features.tasks.service import TasksService
    from src.db.dependencies import get_db

    data = None
    async for db in get_db():
        data = await TasksService.get_actual_tasks(db)

    from .view import View

    app_view = View(page)
    page.add(app_view.main_layout(data))

if __name__ == "__main__":
    ft.app(target=main)
