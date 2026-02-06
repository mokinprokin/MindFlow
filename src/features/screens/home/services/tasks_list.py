import asyncio
from ..components.task_item import TaskItem
from .manager import TasksManager


class TasksListService:
    def __init__(self, tasks_column, page):
        self.tasks_column = tasks_column
        self.page = page

    def converted_tasks(self, data):
        if not data:
            return
        for i, item in enumerate(data):
            self.tasks_column.controls.append(
                TaskItem(
                    time_from=item.time_from,
                    time_to=item.time_to,
                    title=item.task,
                    priority=item.priority,
                    original_index=i,
                    is_completed=getattr(item, "is_done", False),
                    on_task_change=self.handle_task_change,
                )
            )
        self.tasks_column.controls.sort(
            key=lambda x: (
                bool(getattr(x, "is_completed", False)),
                getattr(x, "original_index", 0) or 0,
            )
        )

    def handle_task_change(self, task_item):
        self.page.run_task(
            self.save_task_state,
            task_item.time_from,
            task_item.title,
            task_item.is_completed,
        )

        self.page.run_task(self.deferred_sort)

    async def save_task_state(self, time_from: str, title: str, is_completed: bool):
        await asyncio.wait_for(
            TasksManager.toggle_task_completion(time_from, title, is_completed),
            timeout=3.0,
        )

    async def deferred_sort(self):
        await asyncio.sleep(0.3)

        try:
            self.tasks_column.controls.sort(
                key=lambda x: (
                    getattr(x, "is_completed", False),
                    getattr(x, "original_index", 0),
                )
            )
            self.page.update()
        except Exception:
            pass
