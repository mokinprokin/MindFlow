import flet as ft
from .components import Items
from src.features.sound.service import SoundService

class TaskItem(ft.Container):
    BG_FINAL = "#1A0B2E"
    GLASS_WHITE = "#FFFFFF10"
    ACCENT_PURPLE = "#8E54E9"
    ACCENT_BLUE = "#4776E6"
    TEXT_MUTED = "#FFFFFF70"

    def __init__(
        self, 
        time_from, 
        time_to,
        title, 
        priority="Medium", 
        original_index=0, 
        on_task_change=None,
        is_completed=False,  
    ):
        super().__init__()
        self.time_from = time_from
        self.time_to = time_to
        self.title = title
        self.priority = priority
        self.original_index = original_index if original_index is not None else 0
        self.is_completed = bool(is_completed)
        self.on_task_change = on_task_change

        self.animate_offset = ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT_CUBIC)
        self.animate_opacity = ft.Animation(400, ft.AnimationCurve.EASE_OUT)

        self.check_icon = ft.Icon(
            ft.Icons.CHECK_ROUNDED, size=14, color=ft.Colors.TRANSPARENT
        )
        self.text_title = ft.Text(
            self.title,
            color=ft.Colors.WHITE,
            size=15,
            weight="w500",
        )

        self.checkbox = Items.build_checkbox(
            check_icon=self.check_icon, toggle_check=self.toggle_check
        )

        self.padding = ft.padding.symmetric(horizontal=16, vertical=12)
        self.margin = ft.margin.only(bottom=10)
        self.border_radius = 20
        self.bgcolor = ft.Colors.with_opacity(0.8, "#424242")
        self.border = ft.border.all(1, ft.Colors.WHITE_10)

        p_Colors = {"High": "#FF4B4B", "Medium": "#FF9F2E", "Low": "#00F0FF"}
        p_color = p_Colors.get(priority, "#00F0FF")

        time_display = f"{self.time_from}"

        self.content = ft.Row(
            controls=[
                self.checkbox,
                ft.Column(
                    [
                        ft.Text(time_display, color=ft.Colors.WHITE, size=13, weight="bold"),
                    ],
                    spacing=2,
                    tight=True,
                ),
                ft.Container(),  
                ft.Column(
                    [
                        self.text_title,
                        ft.Text(
                            self._calculate_duration(),
                            color=TaskItem.TEXT_MUTED,
                            size=11,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Container(
                    width=8,
                    height=8,
                    bgcolor=p_color,
                    border_radius=4,
                    shadow=ft.BoxShadow(blur_radius=10, color=p_color),
                ),
            ]
        )
        
        if self.is_completed:
            self.update_ui_state()

    def toggle_check(self, e):
        self.is_completed = not self.is_completed
        SoundService.play_click()
        self.update_ui_state()  
        
        if self.on_task_change:
            self.on_task_change(self)

    def update_ui_state(self):
        if self.is_completed:
            self.checkbox.bgcolor = TaskItem.ACCENT_BLUE
            self.checkbox.border = ft.border.all(1.5, TaskItem.ACCENT_BLUE)
            self.check_icon.color = ft.Colors.WHITE
            self.text_title.style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH, color=TaskItem.TEXT_MUTED
            )
            self.opacity = 0.65
        else:
            self.checkbox.bgcolor = ft.Colors.TRANSPARENT
            self.checkbox.border = ft.border.all(1.5, ft.Colors.WHITE_24)
            self.check_icon.color = ft.Colors.TRANSPARENT
            self.text_title.style = ft.TextStyle(
                decoration=ft.TextDecoration.NONE, color=ft.Colors.WHITE
            )
            self.opacity = 1.0
    def _calculate_duration(self) -> str:
        try:
            from datetime import datetime
            fmt = "%H:%M"
            start = datetime.strptime(self.time_from, fmt)
            end = datetime.strptime(self.time_to, fmt)
            delta = end - start
            total_seconds = int(delta.total_seconds())
            
            if total_seconds < 0:
                total_seconds += 24 * 3600
                
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            parts = []
            if hours > 0:
                parts.append(f"{hours} ч")
            if minutes > 0:
                parts.append(f"{minutes} мин")
                
            return " ".join(parts) if parts else "0 мин"
        except (ValueError, TypeError):
            return "—"