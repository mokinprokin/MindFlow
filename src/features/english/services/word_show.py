import random
from typing import List, Optional
from src.features.english.schemas import WordsShema, WordQuizSchema


class WordShowService:
    @staticmethod
    async def get_all_words(db) -> List[WordsShema]:
        words = await db.words.get_all()
        return words

    @staticmethod
    async def get_word_by_id(db, word_id: int) -> Optional[WordsShema]:
        word = await db.words.get_one_or_none(id=word_id)
        return word

    @staticmethod
    async def get_word_by_english(db, in_english: str) -> Optional[WordsShema]:
        word = await db.words.get_one_or_none(in_english=in_english.strip())
        return word

    @staticmethod
    def check_answer(word: WordQuizSchema, answer: str) -> bool:
        if not word:
            return False
        user_ans = WordShowService._normalize_string(answer)
        valid_options = [word.in_english] + word.in_russian
        for option in valid_options:
            if WordShowService._normalize_string(option) == user_ans:
                return True

        return False

    @staticmethod
    def _normalize_string(text: str) -> str:
        if not text:
            return ""

        normalized = text.strip()

        normalized = normalized.lower()

        while normalized and normalized[-1] in ".,!?;:":
            normalized = normalized[:-1].strip()

        return normalized

    @staticmethod
    def get_correct_translations(word: WordsShema) -> List[str]:
        if not word or not word.in_russian:
            return []
        return word.in_russian.copy()

    @staticmethod
    async def get_words_for_review(db, limit: Optional[int] = None) -> List[WordsShema]:
        words = await db.words.get_words_for_review(limit=limit)
        return words

    @staticmethod
    async def get_quiz_data(db, limit: int = 5) -> List[WordQuizSchema]:
        review_words = await db.words.get_words_for_review(limit=limit)

        quiz_list = []

        for word in review_words:
            quiz_item = WordQuizSchema(
                id=word.id,
                in_english=word.in_english,
                in_russian=word.in_russian,
                pivot="left", 
            )
            quiz_list.append(quiz_item)
        if quiz_list:
            random_index = random.randrange(len(quiz_list))
            quiz_list[random_index].pivot = "right"
        return quiz_list
