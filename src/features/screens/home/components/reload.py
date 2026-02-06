import asyncio
import flet as ft
class ReloadButton(ft.Container):
    def __init__(self, on_reload):
        super().__init__()
        self.on_reload = on_reload  
        self.icon = ft.Icon(
            ft.Icons.REFRESH_ROUNDED, 
            color=ft.Colors.WHITE, 
            size=20
        )
        
        self.content = self.icon
        self.width = 40
        self.height = 40
        self.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
        self.border_radius = 12
        self.border = ft.border.all(1, ft.Colors.WHITE_10)
        self.alignment = ft.Alignment.CENTER
        self.on_click = self.animate_click

        self.rotate = ft.Rotate(0, alignment=ft.Alignment.CENTER)
        self.animate_rotation = ft.Animation(700, ft.AnimationCurve.DECELERATE)
        self.animate = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        

    async def animate_click(self, e):
        self.rotate.angle += 3.14 * 2  
        self.shadow = ft.BoxShadow(blur_radius=15, color="#8E54E9")
        self.update()
        
        if self.on_reload:
            await self.on_reload()
        
        await asyncio.sleep(0.5)
        self.shadow = None
        self.update()