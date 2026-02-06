from src.features.voice.engine import VoiceEngine
from src.features.sound.service import SoundService
from .utils import toggle_flet_window

if __name__ == "__main__":
    engine = VoiceEngine(wakewords=["alexa"], threshold=0.45, gain=1.8)
    

    engine.add_handler(
        "alexa",
        lambda: toggle_flet_window("home", "home", sound_func=lambda: SoundService.play_open())
    )
    
    engine.run()