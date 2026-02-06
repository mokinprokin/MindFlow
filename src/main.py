import logging
from src.scripts.autostart import (
    voice_daily_service,
    english_voice_service,
    notifications_service,
    daily_plan,
)
from src.db.database import init_db
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    # Initialize the SQLite database and run pending migrations via Alembic
    await init_db()

    # Voice Daily Service: Listens for the "Alexa" wake word to
    # automatically toggle the Daily Planner UI window.
    voice_daily_service.setup_startup()

    # Notification Service: Manages background scheduling for:
    # 1. Rest reminders (based on inactivity or interval).
    # 2. Upcoming task alerts (triggered 15 mins before start).
    # 3. Spaced repetition English quizzes (scheduled via chess-order logic).
    # Parameters are configurable via 'scripts/notifications_background.py'.
    notifications_service.setup_startup()

    # English Voice Service: Listens for the "Hey Jarvis" wake word
    # to trigger the 'Add New Word' UI for vocabulary expansion.
    english_voice_service.setup_startup()

    # Daily Plan Service: Performs the initial sync with Google Sheets API
    # to fetch and update local tasks for the current day.
    daily_plan.setup_startup()

    logger.info("Services started successfully")


if __name__ == "__main__":
    asyncio.run(main())
