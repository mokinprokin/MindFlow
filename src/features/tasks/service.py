from ..google.services.google_sheets import GoogleSheetsService
from .schemas import TasksSchema, TasksUpdateSchema
from src.db.dependencies import DBManager
from ..scheduler.service import SchedulerService
from .utils import SyncStateUtil


class TasksService:
    @classmethod
    async def create_tasks(cls, db) -> list[TasksSchema]:
        sheet = await GoogleSheetsService.get_last_sheet()
        if not sheet:
            return []

        data = await GoogleSheetsService.get_sheet_data(sheet.id)
        data_insert = TasksSchema.from_raw_list(data)

        await db.tasks.delete_all()
        await db.tasks.create_bulk(data_insert)
        await db.commit()

        return data_insert

    @classmethod
    async def get_tasks(cls, db) -> list[TasksSchema]:
        sheets = await db.tasks.get_all()
        return [TasksSchema.model_validate(sheet) for sheet in sheets]

    @classmethod
    async def update_task(cls, db, data: TasksUpdateSchema, **kwargs) -> TasksSchema:
        task = await db.tasks.update(data=data, exclude_unset=True, **kwargs)
        await db.commit()
        return TasksSchema.model_validate(task)

    @classmethod
    async def create_task(cls, db, data: TasksSchema):
        await db.tasks.create(data=data)
        await db.commit()
        return data

    @classmethod
    async def get_actual_tasks(cls, db) -> list[TasksSchema]:
        if not SchedulerService.is_sync_time():
            return await cls.get_tasks(db)

        local_now = SchedulerService.get_local_time()
        current_date = local_now.date()

        last_sync = SyncStateUtil.get_last_sync_date()
        if last_sync == current_date:
            return await cls.get_tasks(db)

        tasks = await cls.create_tasks(db)

        if tasks:
            SyncStateUtil.set_last_sync_date(current_date)

        return tasks

    @classmethod
    async def get_unimportant_tasks(cls, db: DBManager) -> list[TasksSchema]:
        tasks = await db.tasks.get_filtered(priority=["Low", "Medium"])
        return tasks

    @classmethod
    async def get_important_tasks(cls, db: DBManager) -> list[TasksSchema]:
        tasks = await db.tasks.get_filtered(priority="High")
        return tasks
