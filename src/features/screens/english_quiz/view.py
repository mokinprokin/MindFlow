import flet as ft
import asyncio
from ..home.constants import ACCENT_BLUE, ACCENT_PURPLE, TEXT_MUTED
from ..home.components.components import Items
from .services.manager import WordManager
from .utils import close_window

class TrainingRow(ft.Column):
    def __init__(self, data, on_submit=None):
        super().__init__()
        self.spacing = 0
        self.data = data
        self.feedback_text = ft.Text(
            "", size=11, weight="w500", opacity=0, no_wrap=True
        )
        self.feedback_container = ft.Container(
            content=self.feedback_text,
            height=16,
            margin=ft.margin.only(bottom=2),
        )
        self.is_submitted = False

        self.input_field = self._build_input(on_submit)

        if data.pivot == "left":
            left_content = ft.Column(
                [self.feedback_container, self.input_field], spacing=0
            )
            right_content = ft.Column(
                [
                    ft.Container(height=16, margin=ft.margin.only(bottom=2)),
                    self._build_text(data.in_russian_text),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            )
        else:
            left_content = ft.Column(
                [
                    ft.Container(height=16, margin=ft.margin.only(bottom=2)),
                    self._build_text(data.in_english),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            )
            right_content = ft.Column(
                [self.feedback_container, self.input_field], spacing=0
            )

        self.main_row = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
            controls=[
                ft.Container(
                    content=ft.Text(
                        f"{data.id}.",
                        size=14,
                        color=ft.Colors.WHITE30,
                        width=30,
                        weight="bold",
                    ),
                    margin=ft.margin.only(top=16 + 10),
                ),
                ft.Container(content=left_content, expand=1),
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.CHEVRON_RIGHT_ROUNDED, color=ft.Colors.WHITE10, size=20
                    ),
                    margin=ft.margin.only(top=16 + 8),
                ),
                ft.Container(content=right_content, expand=1),
            ],
        )

        self.controls = [self.main_row]

    async def focus_input(self):
        await self.input_field.focus()

    def _build_input(self, on_submit):
        return ft.TextField(
            hint_text="...",
            height=38,
            text_size=13,
            content_padding=ft.padding.only(left=10, right=10),
            color="white",
            cursor_color=ACCENT_BLUE,
            bgcolor=ft.Colors.with_opacity(0.1, "black"),
            border_radius=10,
            border_color=ft.Colors.with_opacity(0.15, "white"),
            focused_border_color=ACCENT_BLUE,
            on_submit=on_submit,
        )

    def _build_text(self, text):
        return ft.Container(
            content=ft.Text(text, size=14, weight="w500", color="white", no_wrap=True),
            height=38,
            alignment=ft.Alignment.CENTER_LEFT,
        )


class QuizView:
    def __init__(self, page):
        self.page = page
        self.rows_list = []

    def _apply_row_style(self, row, result: dict):
        is_correct = result["is_correct"]
        
        row.input_field.border_color = ft.Colors.GREEN_400 if is_correct else ft.Colors.RED_400
        row.feedback_text.value = "  ✓ Верно" if is_correct else f"  ✕ Ответ: {result['correct_value']}"
        row.feedback_text.color = ft.Colors.GREEN_400 if is_correct else ft.Colors.RED_400
        row.feedback_text.opacity = 1

    async def _handle_check(self, e=None):
        for row in self.rows_list:
            if row.is_submitted: continue
            
            row.is_submitted = True
            result = await WordManager.process_answer(row.data, row.input_field.value)
            self._apply_row_style(row, result)
            
        self.page.update()

    async def _handle_check_one(self, e):
        current_row = next((r for r in self.rows_list if r.input_field == e.control), None)
        if not current_row or current_row.is_submitted:
            return

        current_row.is_submitted = True
        result = await WordManager.process_answer(current_row.data, current_row.input_field.value)
        self._apply_row_style(current_row, result)

        idx = self.rows_list.index(current_row)
        if idx + 1 < len(self.rows_list):
            await self.rows_list[idx + 1].focus_input()

        self.page.update()


    async def main_layout(self) -> ft.Container:
        rows_data = await WordManager.generate_quiz()
        self.rows_list = []
        for data in rows_data:
            self.rows_list.append(
                TrainingRow(
                    data=data,
                    on_submit=self._handle_check_one,
                )
            )

        close_button = ft.Container(
            content=ft.Icon(ft.Icons.CLOSE_ROUNDED, color=ft.Colors.WHITE30, size=20),
            top=10,
            right=10,
            on_click=lambda e: asyncio.create_task(close_window(self.page)),
            animate=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            on_hover=lambda e: setattr(
                e.control.content,
                "color",
                "white" if e.data == "true" else ft.Colors.WHITE30,
            )
            or e.control.update(),
        )

        return ft.Container(
            expand=True,
            border_radius=35,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=["#232323", "#121212"],
            ),
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.1, "white")),
            blur=ft.Blur(40, 40),
            padding=25,
            content=ft.Stack(
                [
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.PSYCHOLOGY_ALT_ROUNDED,
                                        color=ACCENT_PURPLE,
                                        size=28,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "Quiz Mode",
                                                size=18,
                                                weight="bold",
                                                color="white",
                                            ),
                                            ft.Text(
                                                "Translate 5 words",
                                                size=12,
                                                color=TEXT_MUTED,
                                            ),
                                        ],
                                        spacing=0,
                                    ),
                                ]
                            ),
                            ft.Divider(height=1, color=ft.Colors.WHITE10),
                            ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.ADAPTIVE,
                                controls=[
                                    ft.Container(
                                        content=ft.Column(
                                            controls=self.rows_list, spacing=5
                                        ),
                                        padding=ft.padding.only(
                                            right=20, left=5, bottom=10
                                        ),
                                    )
                                ],
                            ),
                            ft.Container(
                                content=Items.build_button(
                                    name="Проверить результат",
                                    on_click=self._handle_check,
                                ),
                                padding=ft.padding.only(top=5),
                            ),
                        ],
                    ),
                    close_button,
                ]
            ),
        )
