import flet as ft
from .view import View
async def main(page: ft.Page):
    from .services.window import WindowService
    WindowService.apply_settings(page)
    page.update()
    app_view = View(page)
    page.add(app_view.main_layout())
    page.update()

if __name__ == "__main__":
    ft.run(main=main)
