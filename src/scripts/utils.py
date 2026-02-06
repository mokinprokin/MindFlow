import subprocess
import sys
import os
from typing import Dict
from src.features.sound.service import SoundService

_active_processes: Dict[str, subprocess.Popen] = {}


def toggle_flet_window(dir_name: str, file_name: str, sound_func: callable):
    global _active_processes
    window_key = f"{dir_name}.{file_name}"

    process = _active_processes.get(window_key)

    if process and process.poll() is None:
        SoundService.play_close()
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(process.pid)],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        else:
            process.terminate()

        _active_processes[window_key] = None
    else:
        sound_func()
        module_path = f"src.features.screens.{dir_name}.{file_name}"

        new_process = subprocess.Popen(
            [sys.executable, "-m", module_path],
            cwd=os.getcwd(),
            creationflags=subprocess.CREATE_NO_WINDOW | 0x00000200,
        )
        _active_processes[window_key] = new_process
