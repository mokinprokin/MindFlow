import logging
import os
import sys
import getpass
from pathlib import Path


class ScriptsService:
    logger = logging.getLogger(__name__)

    def __init__(
        self, bat_name: str, vbs_name: str, script_name: str, shortcut_name: str
    ):
        self.bat_name = bat_name
        self.vbs_name = vbs_name
        self.script_name = script_name
        self.shortcut_name = shortcut_name

    def setup_startup(self):
        project_root = Path(__file__).parent.parent.parent.absolute()
        python_exe = Path(sys.executable).absolute()

        bat_path = project_root / f"./src/scripts/other/{self.bat_name}.bat"
        vbs_path = project_root / f"./src/scripts/other/{self.vbs_name}.vbs"

        bat_content = (
            f"@echo off\n"
            f'cd /d "{project_root}"\n'
            f'"{python_exe}" -m src.scripts.{self.script_name}'
        )

        vbs_content = (
            f'Set WshShell = CreateObject("Wscript.Shell")\n'
            f'WshShell.Run "cmd /c ""{bat_path}""", 0, False'
        )

        try:
            bat_path.write_text(bat_content, encoding="utf-8")
            vbs_path.write_text(vbs_content, encoding="utf-8")

            user_name = getpass.getuser()
            startup_folder = Path(
                f"C:/Users/{user_name}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
            )

            shortcut_path = startup_folder / f"{self.shortcut_name}.lnk"
            ps_command = (
                f"$WshShell = New-Object -ComObject WScript.Shell; "
                f"$Shortcut = $WshShell.CreateShortcut('{shortcut_path}'); "
                f"$Shortcut.TargetPath = '{vbs_path}'; "
                f"$Shortcut.WorkingDirectory = '{project_root}'; "
                f"$Shortcut.Save()"
            )

            os.system(f'powershell -command "{ps_command}"')

            ScriptsService.logger.info(f"--- Instalation complete ---")
            ScriptsService.logger.info(f"Project: {project_root}")
            ScriptsService.logger.info(f"shortcut created in: {shortcut_path}")

        except Exception as e:
            ScriptsService.logger.error(f"Error instalation: {e}")


daily_plan = ScriptsService(
    bat_name="run_sync_hidden",
    vbs_name="silent_start_sync",
    script_name="fetch_tasks",
    shortcut_name="daily_plan",
)

voice_daily_service = ScriptsService(
    bat_name="run_daily_voice_hidden",
    vbs_name="silent_start_voice_daily",
    script_name="voice_background_daily",
    shortcut_name="daily_plan_voice",
)
english_voice_service = ScriptsService(
    bat_name="run_english_voice_hidden",
    vbs_name="silent_start_voice_english",
    script_name="voice_background_english",
    shortcut_name="daily_plan_english",
)
notifications_service = ScriptsService(
    bat_name="run_notifications_hidden",
    vbs_name="silent_start_notifications",
    script_name="notifications_background",
    shortcut_name="daily_plan_notifications",
)

if __name__ == "__main__":
    notifications_service.setup_startup()
