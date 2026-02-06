from src.features.tasks.schemas import TasksUpdateSchema
from src.features.tasks.service import TasksService
from src.db.dependencies import get_db


class TasksManager:
    @staticmethod
    async def fetch_fresh_data():
        async for db in get_db():
            try:
                return await TasksService.create_tasks(db)
            except:
                raise

    @classmethod
    async def update_task_by_criteria(
        cls, time_from: str, task_title: str, update_data: TasksUpdateSchema
    ) -> bool:
        async for db in get_db():
            try:
                return await TasksService.update_task(
                    db=db, 
                    time_from=time_from, 
                    task=task_title, 
                    data=update_data
                )
            except Exception as e:
                print(f"Error updating task {task_title} at {time_from}: {e}")
                return False

    @classmethod
    async def toggle_task_completion(cls, time_from: str, task_title: str, is_completed: bool) -> bool:
        update_data = TasksUpdateSchema(is_done=is_completed)
        async for db in get_db():
            try:
                result = await TasksService.update_task(
                    db=db, time_from=time_from, task=task_title, data=update_data
                )
                return result
            except Exception as e:
                print(f"Database error: {e}")
                return False