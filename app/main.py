from __future__ import annotations
import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.config import settings
from app.middlewares import SessionMiddleware
from app.routers.project import router as project_router
from app.routers.sales_join import router as sales_join_router
from app.routers.sales import router as sales_router
from app.database import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main() -> None:
    try:
        logger.info("Starting DoxSalesBot...")
        await init_db()
        logger.info("Database initialized")
        
        bot = Bot(token=settings.bot_token)
        dp = Dispatcher()
        dp.update.middleware(SessionMiddleware())
        dp.include_router(project_router)
        dp.include_router(sales_join_router)
        dp.include_router(sales_router)
        
        logger.info("Bot started successfully")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
