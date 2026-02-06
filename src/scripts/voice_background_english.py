import threading
import keyboard
from src.features.voice.engine import VoiceEngine
from src.features.sound.service import SoundService
from .utils import toggle_flet_window
import time

def create_cooldown_wrapper(func, cooldown_seconds=1.0):
    last_call_time = 0.0

    def wrapper(*args, **kwargs):
        nonlocal last_call_time
        current_time = time.perf_counter()
        
        if current_time - last_call_time >= cooldown_seconds:
            last_call_time = current_time
            return func(*args, **kwargs)
        return None

    return wrapper


def on_toggle():
    toggle_flet_window(
        "english_quiz", 
        "quiz_home", 
        lambda: SoundService.play_open_english()
    )

protected_toggle = create_cooldown_wrapper(on_toggle, cooldown_seconds=2.0)

def setup_hotkeys():
    keyboard.add_hotkey("\\", protected_toggle)
    keyboard.wait()

if __name__ == "__main__":
    hotkey_thread = threading.Thread(target=setup_hotkeys, daemon=True)
    hotkey_thread.start()
    engine_english = VoiceEngine(
        wakewords=["hey_jarvis"],
        threshold=0.45,
        gain=1.8,
    )
    engine_english.add_handler(
        "hey_jarvis",
        lambda: toggle_flet_window(
            "english_home", "english_home", lambda: SoundService.play_open_english()
        ),
    )

    try:
        engine_english.run()
    except KeyboardInterrupt:
        print("Stopped...")
