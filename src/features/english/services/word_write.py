from datetime import datetime, timedelta, timezone, date
from typing import List, Union
from src.features.english.schemas import WordCreateSchema, WordsShema, WordFullUpdate
from src.features.english.schemas import WordUpdateSchema
from src.db.db_manager import DBManager


class WordWriteService:
    @staticmethod
    async def create_word(
        db, in_english: str, in_russian: Union[str, List[str]]
    ) -> WordsShema:
        translations = WordWriteService._normalize_translations(in_russian)

        word_data = WordCreateSchema(
            in_english=in_english.strip(), in_russian=translations
        )

        existing_word = await db.words.get_one_or_none(in_english=word_data.in_english)
        if existing_word:
            existing_translations = set(existing_word.in_russian)
            new_translations = set(translations)
            all_translations = list(existing_translations | new_translations)

            update_data = WordUpdateSchema(in_russian=all_translations)
            updated_word = await db.words.update(
                data=update_data, in_english=word_data.in_english
            )
            await db.commit()
            return updated_word

        created_word = await db.words.create(data=word_data)
        await db.commit()
        return created_word

    @staticmethod
    def _normalize_translations(in_russian: Union[str, List[str]]) -> List[str]:

        if isinstance(in_russian, list):
            return [
                translation.strip() for translation in in_russian if translation.strip()
            ]

        if isinstance(in_russian, str):
            translations = [t.strip() for t in in_russian.split(",") if t.strip()]
            return translations if translations else [in_russian.strip()]

        raise ValueError(
            f"in_russian должен быть строкой или списком, получен: {type(in_russian)}"
        )

    @staticmethod
    async def create_word_bulk(db, words: List[dict]) -> dict:
        word_schemas = []
        for word_data in words:
            translations = WordWriteService._normalize_translations(
                word_data.get("in_russian", "")
            )
            word_schema = WordCreateSchema(
                in_english=word_data.get("in_english", "").strip(),
                in_russian=translations,
            )
            word_schemas.append(word_schema)

        await db.words.create_bulk(word_schemas)
        await db.commit()
        return {"response": "ok", "created": len(word_schemas)}

    @staticmethod
    async def update_correct_word(db: DBManager, word_id: int, is_correct: bool):
        word_model = await db.words.get_one_or_none(id=word_id)
        if not word_model:
            raise ValueError(f"Word with id {word_id} not found")

        if not is_correct:
            word_model.repetition_count = 0
            word_model.interval = 0
            word_model.ease_factor -= 0.2
        else:
            if word_model.repetition_count == 0:
                word_model.interval = 1
            elif word_model.repetition_count == 1:
                word_model.interval = 6
            else:
                word_model.interval = round(
                    word_model.interval * word_model.ease_factor
                )

            word_model.repetition_count += 1
            word_model.ease_factor += 0.1

        word_model.ease_factor = max(1.3, min(word_model.ease_factor, 2.5))

        now = datetime.now(timezone.utc)
        today = date.today()
        word_model.last_review = now
        word_model.next_review = today + timedelta(days=word_model.interval)
        update_data = WordFullUpdate.model_validate(
            word_model.model_dump(exclude={"id", "created_at"})
        )
        await db.words.update(data=update_data, id=word_model.id, exclude_unset=True)
        await db.commit()
        return word_model
