import asyncio
import logging
from src.db.dependencies import get_db
from src.features.tasks.service import TasksService

logger = logging.getLogger(__name__)


async def run_once():
    logging.info("Script started...")
    await asyncio.sleep(15)
    try:
        async for db in get_db():
            tasks = await TasksService.get_actual_tasks(db)

            if tasks:
                logging.info(f"Success! Tasks: {len(tasks)}")
            break

    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
    finally:
        logging.info("Script executed")


if __name__ == "__main__":
    asyncio.run(run_once())
