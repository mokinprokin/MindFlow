from datetime import datetime
import flet as ft
from ..constants import *


class Items:
    @classmethod
    def build_checkbox(cls, check_icon, toggle_check) -> ft.Container:
        return ft.Container(
            content=check_icon,
            width=24,
            height=24,
            border_radius=12,
            border=ft.border.all(1.5, ft.Colors.WHITE24),
            alignment=ft.Alignment.CENTER,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            on_click=toggle_check,
        )

    @classmethod
    def build_header(cls, reload_button: ft.Control) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=15,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.CALENDAR_MONTH, color="white", size=30
                            ),
                            bgcolor=ft.Colors.with_opacity(0.2, "white"),
                            padding=12,
                            border_radius=15,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    datetime.now().strftime("%d %B"),
                                    size=18,
                                    weight="bold",
                                    color="white",
                                ),
                                ft.Text("Dashboard", color="white54", size=14),
                            ],
                            spacing=0,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                ),
                reload_button,
            ],
        )

    @classmethod
    def build_button(cls, name: str, on_click=None) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ADD_ROUNDED, color="white", size=20),
                    ft.Text(name, color="white", weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.Alignment.CENTER,
            height=40,
            border_radius=20,
            gradient=ft.LinearGradient(
                colors=[ACCENT_PURPLE, ACCENT_BLUE],
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
            ),
            on_click=on_click,
            shadow=ft.BoxShadow(
                blur_radius=20,
                color=ft.Colors.with_opacity(0.3, ACCENT_PURPLE),
                offset=ft.Offset(0, 10),
            ),
        )
