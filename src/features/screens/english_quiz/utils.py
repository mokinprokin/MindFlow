import asyncio
import flet as ft

_is_closing = False


async def close_window(page: ft.Page):
    global _is_closing
    if _is_closing:
        return

    _is_closing = True

    page.window.visible = False
    page.window.update()

    await asyncio.sleep(0.1)
    await page.window.destroy()


async def handle_key_event(page: ft.Page, e: ft.KeyboardEvent):
    if (e.key == "\\" or e.key == "Backslash") and not _is_closing:
        await close_window(page)
