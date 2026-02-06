import flet as ft
from ..home.constants import ACCENT_BLUE, ACCENT_PURPLE
from .services.manager import WordManager


class View:
    def __init__(self, page):
        self.page = page
        self.en_input = self._build_input(
            "English word...",
            ft.Icons.LANGUAGE,
            on_submit=lambda _: self.ru_input.focus(),
        )
        self.ru_input = self._build_input(
            "Перевод на русский...", ft.Icons.TRANSLATE, on_submit=self._handle_save
        )

    async def _handle_save(self, e=None):
        en_word = self.en_input.value
        ru_word = self.ru_input.value

        if not en_word or not ru_word:
            self.ru_input.border_color = ft.Colors.RED_400
            self.page.update()
            return

        await WordManager.create_dictionary(en_word, ru_word)

        self.en_input.value = ""
        self.ru_input.value = ""
        self.ru_input.border_color = ft.Colors.with_opacity(0.1, "white")
        self.en_input.focus()

    def main_layout(self) -> ft.Container:
        return ft.Container(
            expand=True,
            border_radius=ft.BorderRadius(40, 0, 7, 0),
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
                colors=["#292929", "#313131"],
            ),
            blur=ft.Blur(100, 100),
            padding=25,
            shadow=ft.BoxShadow(
                blur_radius=40,
                color=ft.Colors.with_opacity(0.75, ACCENT_PURPLE),
                offset=ft.Offset(0, 15),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    ft.Text("Add to Dictionary", size=18, weight="bold", color="white"),
                    self.en_input,
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.SWAP_VERT_ROUNDED, color=ACCENT_BLUE, size=24
                        ),
                        padding=5,
                        bgcolor=ft.Colors.with_opacity(0.1, "white"),
                        border_radius=10,
                    ),
                    self.ru_input,
                    ft.Container(height=2),
                    self._build_add_button(),
                ],
            ),
        )

    def _build_input(self, hint, icon, on_submit=None):
        return ft.TextField(
            hint_text=hint,
            prefix_icon=icon,
            text_size=14,
            height=45,
            width=365,
            hint_style=ft.TextStyle(color=ft.Colors.WHITE30),
            color="white",
            cursor_color=ACCENT_BLUE,
            bgcolor=ft.Colors.with_opacity(0.05, "white"),
            border_radius=15,
            border_color=ft.Colors.with_opacity(0.1, "white"),
            focused_border_color=ACCENT_BLUE,
            content_padding=10,
            on_submit=on_submit,
        )

    def _build_add_button(self):
        return ft.Container(
            content=ft.Text("Добавить в словарь", color="white", weight="bold"),
            alignment=ft.Alignment.CENTER,
            height=40,
            border_radius=15,
            gradient=ft.LinearGradient(
                colors=[ACCENT_PURPLE, ACCENT_BLUE],
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
            ),
            on_click=self._handle_save,
            shadow=ft.BoxShadow(
                blur_radius=20,
                color=ft.Colors.with_opacity(0.3, ACCENT_PURPLE),
                offset=ft.Offset(0, 8),
            ),
        )
