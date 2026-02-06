import flet as ft

class WindowService:
    WIDTH = 580
    HEIGHT = 450 
    PADDING = 0
    SPACING = 0

    @staticmethod
    def apply_settings(page: ft.Page):
        WindowService._set_position(page)
        page.title = "Quiz Mode"
        page.window.width = WindowService.WIDTH
        page.window.height = WindowService.HEIGHT
        page.bgcolor = ft.Colors.TRANSPARENT
        page.window.bgcolor = ft.Colors.TRANSPARENT
        page.window.skip_task_bar = True
        page.window.frameless = True
        page.window.always_on_top = True
        page.window.resizable = False
        page.padding = WindowService.PADDING
        page.spacing = WindowService.SPACING

    @staticmethod
    def _set_position(page: ft.Page):
        page.window.left = 1920/2 - WindowService.WIDTH*0.47
        page.window.top = 1080 - WindowService.HEIGHT - 48
        page.update()