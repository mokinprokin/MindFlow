from datetime import datetime
from src.features.tasks.service import TasksService
from typing import List


class RepetitionService:
    @classmethod
    async def calculate_daily_schedule(
        cls, db, max_notifications: int
    ) -> List[datetime]:
        today = datetime.now().date()
        tasks = await TasksService.get_actual_tasks(db)
        scheduled_notification_tasks = []
        notifications_scheduled = 0
        should_show_by_order = True
        force_next = False

        for task in tasks:
            if notifications_scheduled >= max_notifications:
                break
            if task.priority.lower() == "high":
                force_next = True
                continue

            if should_show_by_order or force_next:
                try:
                    task_time = datetime.strptime(task.time_from, "%H:%M").time()
                except ValueError:
                    task_time = datetime.strptime(task.time_from, "%H:%M:%S").time()
                full_datetime = datetime.combine(today, task_time)
                scheduled_notification_tasks.append(full_datetime)
                notifications_scheduled += 1

                should_show_by_order = False
                force_next = False
            else:
                should_show_by_order = True

        return scheduled_notification_tasks
