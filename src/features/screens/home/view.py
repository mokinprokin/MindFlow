import flet as ft

from .constants import *
from .components.components import Items
from .components.reload import ReloadButton
from .services.tasks_list import TasksListService
from .services.manager import TasksManager


class View:
    def __init__(self, page):
        self.page = page
        self.tasks_container = ft.Stack(expand=True)
        self.tasks_column = ft.Column(
            expand=True, scroll=ft.ScrollMode.HIDDEN, spacing=0
        )
        self.loader = ft.Container(
            content=ft.ProgressRing(color="#8E54E9", width=30, height=30),
            alignment=ft.Alignment.CENTER,
            visible=False,
        )

    async def handle_reload(self):
        self.loader.visible = True
        self.tasks_column.opacity = 0.3
        self.page.update()

        try:
            new_data = await TasksManager.fetch_fresh_data()
            self.tasks_column.controls.clear()
            TasksListService(self.tasks_column, self.page).converted_tasks(new_data)

        except Exception as e:
            print(f"Error reloading: {e}")
        finally:
            self.loader.visible = False
            self.tasks_column.opacity = 1
            self.page.update()



    def main_layout(self, data) -> ft.Container:
        TasksListService(self.tasks_column, self.page).converted_tasks(data)
        self.tasks_container.controls = [self.tasks_column, self.loader]
        return ft.Container(
            expand=True,
            border_radius=ft.BorderRadius(40,0,7,0),
            border=ft.border.Border(
                top=ft.BorderSide(1.8, ft.Colors.with_opacity(0.8, "#4B4B4B")),
                left=ft.BorderSide(1.8, ft.Colors.with_opacity(0.8, "#4B4B4B")),
                right=ft.BorderSide(1.8, ft.Colors.with_opacity(0.8, "#4B4B4B")),
                bottom=ft.BorderSide(0, ft.Colors.TRANSPARENT),
            ),
            bgcolor=ft.Colors.with_opacity(0.85, "#0A0E14"), 
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=["#292929", "#313131"]
            ),
            blur=ft.Blur(100, 100),
            padding=25,
            
            shadow=ft.BoxShadow(
                blur_radius=20, 
                color=ft.Colors.with_opacity(0.3, "#000000"),
                offset=ft.Offset(10, 10)
            ),
            content=ft.Column(
                controls=[
                    Items.build_header(ReloadButton(on_reload=self.handle_reload)),
                    ft.Container(height=10),
                    ft.Container(content=self.tasks_container, expand=True),
                    Items.build_button(name="New task"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
