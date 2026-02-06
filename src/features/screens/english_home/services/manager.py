from src.db.dependencies import get_db
from src.features.english.services.word_write import WordWriteService


class WordManager:

    @classmethod
    async def create_dictionary(cls, in_englsh, in_russian):
        async for db in get_db():
            try:
                return await WordWriteService.create_word(db, in_englsh, in_russian)
            except Exception as e:
                print(f"Error creating")
                return False
