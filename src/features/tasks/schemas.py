from typing import Any, List
from pydantic import BaseModel, ConfigDict


class TasksSchema(BaseModel):
    time_from: str
    time_to: str
    task: str
    priority: str
    is_done: bool | None = None
    model_config = ConfigDict(extra="ignore")

    @classmethod
    def from_raw_list(cls, sheet_data: List[List[Any]]) -> List["TasksSchema"]:
        if not sheet_data or len(sheet_data) < 2:
            return []

        rows = sheet_data[1:]

        result = []
        for row in rows:
            while len(row) < 4:
                row.append("")

            data_dict = {
                "time_from": row[0],
                "time_to": row[1],
                "task": row[2],
                "priority": row[3],
                "is_done": False,
            }

            try:
                result.append(cls.model_validate(data_dict))
            except Exception as e:
                pass

        return result


class TasksUpdateSchema(BaseModel):
    time: str | None = None
    task: str | None = None
    priority: str | None = None
    is_done: bool | None = None
    model_config = ConfigDict(extra="ignore")


class TasksDifferenceSchema(BaseModel):
    id: int
    is_different: bool
    model_config = ConfigDict(from_attributes=True)


class TasksResponseSchema(TasksSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)