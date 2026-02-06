import logging
from datetime import datetime
import asyncio
from typing import List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.features.sound.service import SoundService
from src.db.dependencies import get_db
from src.features.scheduler.service import SchedulerService
from src.features.english.services.repetition import RepetitionService
from src.scripts.utils import toggle_flet_window

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, task_reminder_min, rest_notification_min):
        self.rest_notification_min = rest_notification_min
        self.task_reminder_min = task_reminder_min
        self._last_notified_task_id: int | None = None
        self._last_rest_notification: datetime | None = None
        self._scheduled_repetitions: List[datetime] = []
        self._lock = asyncio.Lock()
        self.scheduler = AsyncIOScheduler(
            job_defaults={"coalesce": True, "max_instances": 1, "misfire_grace_time": 5}
        )

    async def check_and_play_task_reminder(self):
        async with self._lock:
            current_time = SchedulerService.get_local_time()
            async for db in get_db():
                task_diff = await db.tasks.check_task_transition(
                    current_time, self.task_reminder_min
                )

                if (
                    task_diff.is_different
                    and task_diff.id != self._last_notified_task_id
                ):
                    SoundService.play_reminder()
                    await asyncio.sleep(4)
                    self._last_notified_task_id = task_diff.id

                elif not task_diff.id:
                    self._last_notified_task_id = None

    async def check_and_play_rest_reminder(self):
        async with self._lock:
            current_time = SchedulerService.get_local_time()

            async for db in get_db():
                current_remind_task = await db.tasks.get_current_task_if_not_high(
                    current_time
                )

                if current_remind_task is not None:
                    should_notify = False
                    if self._last_rest_notification is None:
                        should_notify = True
                    else:
                        delta = current_time - self._last_rest_notification
                        if delta.total_seconds() / 60 >= self.rest_notification_min:
                            should_notify = True
                    if should_notify:
                        SoundService.play_rest_reminder()
                        await asyncio.sleep(4)
                        self._last_rest_notification = current_time

    async def init_repetition_schedule(self):
        async for db in get_db():
            self._scheduled_repetitions = (
                await RepetitionService.calculate_daily_schedule(
                    db, max_notifications=5
                )
            )

    async def check_and_play_repetition(self):
        async with self._lock:
            current_time = SchedulerService.get_local_time().replace(tzinfo=None)
            for i in range(len(self._scheduled_repetitions) - 1, -1, -1):
                scheduled_time = self._scheduled_repetitions[i]
                print(scheduled_time)
                diff_seconds = abs((current_time - scheduled_time).total_seconds())
                if diff_seconds <= 300:

                    toggle_flet_window(
                        dir_name="english_quiz",
                        file_name="quiz_home",
                        sound_func=lambda: SoundService.play_open_english(),
                    )
                    await asyncio.sleep(4)

                    self._scheduled_repetitions.pop(i)

                    break

    async def setup_startup(
        self,
        enable_tasks: bool = True,
        enable_rest: bool = True,
        enable_repetition: bool = True,
    ):
        if enable_repetition:
            await self.init_repetition_schedule()
            self.scheduler.add_job(
                self.check_and_play_repetition,
                IntervalTrigger(minutes=2, jitter=8),
                id="repetition_schedule",
                replace_existing=True,
            )
        if enable_tasks:
            self.scheduler.add_job(
                self.check_and_play_task_reminder,
                IntervalTrigger(seconds=128, jitter=4),
                id="upcoming_tasks",
                replace_existing=True,
            )
        if enable_rest:
            self.scheduler.add_job(
                self.check_and_play_rest_reminder,
                IntervalTrigger(seconds=180, jitter=9),
                id="rest_reminder",
                replace_existing=True,
            )

        self.scheduler.start()
