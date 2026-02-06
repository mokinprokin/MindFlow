import datetime

from tzlocal import get_localzone
from src.config import settings

class SchedulerService:
    @staticmethod
    def get_local_time() -> datetime.datetime:
        local_tz = get_localzone()
        return datetime.datetime.now(local_tz)

    @classmethod
    def is_sync_time(cls) -> bool:
        now = cls.get_local_time()
        return settings.SYNC_START_HOUR <= now.hour < settings.SYNC_END_HOUR

