from typing import List
from src.db.repositories.base import BaseRepository
from .model import WordsModel
from .schemas import WordsShema
from datetime import date
from sqlalchemy import select


class WordsRepository(BaseRepository):
    model = WordsModel
    schema = WordsShema

    async def get_words_for_review(self, limit: int | None = None) -> List[WordsShema]:
        today = date.today()

        query = (
            select(WordsModel)
            .where(WordsModel.next_review <= today)
            .order_by(WordsModel.repetition_count.desc(), WordsModel.next_review.asc())
        )
        
        if limit:
            query = query.limit(limit)

        result = await self.session.execute(query)
        words = result.scalars().all()
        return [WordsShema.model_validate(word, from_attributes=True) for word in words]