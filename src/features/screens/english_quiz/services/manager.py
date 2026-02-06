from src.db.dependencies import get_db
from src.features.english.services.word_show import WordShowService
from src.features.english.services.word_write import WordWriteService
import asyncio


class WordManager:

    @classmethod
    async def generate_quiz(cls):
        async for db in get_db():
            try:
                return await WordShowService.get_quiz_data(db, limit=5)
            except Exception as e:
                print(f"Error creating {e}")
                return False

    @classmethod
    async def update_word(cls, word_id: int, is_correct: bool):
        async for db in get_db():
            try:
                result = await WordWriteService.update_correct_word(
                    db, word_id, is_correct
                )
                await db.commit()
                return result
            except Exception as e:
                print(f"Error creating {e}")
                return False
    @classmethod
    async def process_answer(cls,row_data, user_answer: str):
        is_correct = WordShowService.check_answer(row_data, user_answer.strip())
        await cls.update_word(row_data.id, is_correct)
        correct_val = (
            row_data.in_russian_text
            if row_data.pivot == "right"
            else row_data.in_english
        )
        
        return {
            "is_correct": is_correct,
            "correct_value": correct_val
        }

# async def main():
#     quiz = await WordManager.generate_quiz()
#     print(quiz)


# if __name__ == "__main__":
#     asyncio.run(main())
