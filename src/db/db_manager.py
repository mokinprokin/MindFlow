from src.features.tasks.repository import TasksRepository
from src.features.english.repository import WordsRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    @property
    def tasks(self):
        return TasksRepository(self.session)

    @property
    def words(self):
        return WordsRepository(self.session)
