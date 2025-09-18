from __future__ import annotations
import asyncio
from aiogram import Bot, Dispatcher
from app.config import settings
from app.middlewares import SessionMiddleware
from app.routers.project import router as project_router
from app.routers.sales_join import router as sales_join_router
from app.routers.sales import router as sales_router
from app.database import init_db

async def main() -> None:
    await init_db()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.update.middleware(SessionMiddleware())
    dp.include_router(project_router)
    dp.include_router(sales_join_router)
    dp.include_router(sales_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
