import flet as ft

class WindowService:
    WIDTH = 400
    HEIGHT = 320
    PADDING = 0
    SPACING = 0

    @staticmethod
    def get_screen_size():
        return 1920, 1080

    @staticmethod
    def apply_settings(page: ft.Page):
        WindowService._set_position(page)
        page.title = "English"
        page.window.width = WindowService.WIDTH
        page.window.height = WindowService.HEIGHT

        page.bgcolor = ft.Colors.TRANSPARENT
        page.window.bgcolor = ft.Colors.TRANSPARENT
        page.window.skip_task_bar = True
        page.window.frameless = True
        page.window.title_bar_hidden = True
        page.window.always_on_top = True
        page.window.resizable = False

        page.padding = WindowService.PADDING
        page.spacing = WindowService.SPACING

    @staticmethod
    def _set_position(page: ft.Page):
        width, height = WindowService.get_screen_size()
        page.window.left = width - WindowService.WIDTH
        page.window.top = height - WindowService.HEIGHT - 48
        page.update()