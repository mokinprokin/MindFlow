from datetime import datetime, timedelta

from sqlalchemy import and_, select, text
from src.db.repositories.base import BaseRepository
from .model import TasksModel
from .schemas import TasksSchema, TasksDifferenceSchema, TasksResponseSchema


class TasksRepository(BaseRepository):
    model = TasksModel
    schema = TasksSchema

    async def check_task_transition(
        self, start_time: datetime, reminder_minutes: int
    ) -> TasksDifferenceSchema:
        fmt = "%H:%M:%S"
        start_time_str = start_time.strftime(fmt)
        plus_15_str = (start_time + timedelta(minutes=reminder_minutes)).strftime(fmt)

        t1 = self.model.__table__.alias("current_task")
        t2 = self.model.__table__.alias("next_task")

        stmt = (
            select(t2.c.id, (t1.c.task != t2.c.task).label("is_different"))
            .select_from(t1)
            .join(t2, text("1=1"))
            .where(
                and_(
                    t1.c.time_from <= start_time_str,
                    t1.c.time_to > start_time_str,
                    t2.c.time_from <= plus_15_str,
                    t2.c.time_to > plus_15_str,
                )
            )
            .limit(1)
        )

        result = await self.session.execute(stmt)
        row = result.first()

        if not row:
            return TasksDifferenceSchema(id=0, is_different=False)

        return TasksDifferenceSchema.model_validate(row._asdict())

    async def get_current_task_if_not_high(
        self, current_time: datetime
    ) -> TasksResponseSchema | None:
        fmt = "%H:%M:%S"
        current_time_str = current_time.strftime(fmt)

        stmt = (
            select(self.model)
            .where(
                and_(
                    TasksModel.time_from <= current_time_str,
                    TasksModel.time_to > current_time_str,
                    TasksModel.priority != "High",
                )
            )
            .limit(1)
        )
        result = await self.session.execute(stmt)
        task_obj = result.scalars().one_or_none()

        if task_obj:
            return TasksResponseSchema.model_validate(task_obj)

        return None
