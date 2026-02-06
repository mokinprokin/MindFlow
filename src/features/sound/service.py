import logging
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from typing import Dict, Tuple
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SoundService:
    _sounds_dir = Path(__file__).parent / "sounds"
    _cache: Dict[str, Tuple[np.ndarray, int]] = {}

    @classmethod
    def _get_sound_path(cls, filename: str) -> Path:
        return cls._sounds_dir / filename

    @classmethod
    def load_sound(cls, filename: str):
        if filename not in cls._cache:
            path = cls._get_sound_path(filename)
            try:
                data, fs = sf.read(str(path))
                cls._cache[filename] = (data, fs)
                logger.info(f"Sound cached: {filename}")
            except Exception as e:
                logger.error(f"Sound error {filename}: {e}")

    @classmethod
    def play_sound(cls, filename: str, blocking: bool = False):
        if filename not in cls._cache:
            cls.load_sound(filename)

        if filename in cls._cache:
            data, fs = cls._cache[filename]
            try:
                sd.play(data, fs)
                if blocking:
                    sd.wait()
            except Exception as e:
                logger.error(f"Error sound palyback {filename}: {e}")
        else:
            logger.warning(f"Sound {filename} doesnt exists")

    @classmethod
    def play_click(cls):
        cls.play_sound("click.mp3")

    @classmethod
    def play_open(cls):
        cls.play_sound("open.mp3")

    @classmethod
    def play_close(cls):
        cls.play_sound("close.mp3")

    @classmethod
    def play_reminder(cls):
        cls.play_sound("reminder.mp3")

    @classmethod
    def play_open_english(cls):
        cls.play_sound("open_english.mp3")

    @classmethod
    def play_rest_reminder(cls):
        cls.play_sound("rest.mp3")

    @classmethod
    def stop_all(cls):
        sd.stop()
