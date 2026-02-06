import logging
import asyncio
from src.features.notifications.service import NotificationService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    try:
        await NotificationService(
            task_reminder_min=15, rest_notification_min=60
        ).setup_startup(enable_tasks=True, enable_rest=True, enable_repetition=True)
        logger.info("Notification Service is running. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(3600)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Starting Error: {e}", exc_info=True)
