from __future__ import annotations
from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal

class SessionMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        async with SessionLocal() as session:
            data["session"] = session  # type: AsyncSession
            return await handler(event, data)
