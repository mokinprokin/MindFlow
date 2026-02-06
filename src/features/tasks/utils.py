import json
from pathlib import Path
from datetime import date


class SyncStateUtil:
    STATE_FILE = Path("./src/data/sync_state.json")

    @classmethod
    def get_last_sync_date(cls) -> date | None:
        if not cls.STATE_FILE.exists():
            return None
        try:
            data = json.loads(cls.STATE_FILE.read_text())
            return date.fromisoformat(data.get("last_sync"))
        except (json.JSONDecodeError, ValueError):
            return None

    @classmethod
    def set_last_sync_date(cls, sync_date: date):
        cls.STATE_FILE.parent.mkdir(exist_ok=True)
        data = {"last_sync": sync_date.isoformat()}
        cls.STATE_FILE.write_text(json.dumps(data))
