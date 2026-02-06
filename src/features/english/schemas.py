from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, model_validator


class WordCreateSchema(BaseModel):
    in_english: str 
    in_russian: List[str]

    class Config:
        from_attributes = True


class WordUpdateSchema(BaseModel):

    in_english: Optional[str] = None
    in_russian: Optional[List[str]] = None

    class Config:
        from_attributes = True


class WordsShema(BaseModel):

    id: int
    in_english: str
    in_russian: List[str]
    next_review: date
    interval: int
    ease_factor: float
    repetition_count: int
    last_review: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class WordFullUpdate(BaseModel):
    in_english: str
    in_russian: List[str]
    next_review: date
    interval: int
    ease_factor: float
    repetition_count: int
    last_review: Optional[datetime] = None

    class Config:
        from_attributes = True


class WordQuizSchema(BaseModel):
    id: int
    in_english: str
    in_russian: List[str]
    pivot: str
    in_russian_text: str = ""

    @model_validator(mode="after")
    def set_russian_text(self):
        if self.in_russian:
            self.in_russian_text = ", ".join(self.in_russian)
        return self
