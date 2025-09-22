from __future__ import annotations
import secrets
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Channel, Invite, User

router = Router(name="project")

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in {"administrator", "creator"}
    except Exception:
        return False

@router.message(Command("enable_project"))
async def enable_project(message: Message, bot: Bot, session: AsyncSession):
    if message.chat.type not in {"supergroup", "group", "channel"}:
        return await message.reply("Эту команду нужно вызывать в канале/группе.")
    if not await is_admin(bot, message.chat.id, message.from_user.id):
        return await message.reply("Только админ канала может это сделать.")
    ch = (await session.execute(select(Channel).where(Channel.telegram_chat_id == message.chat.id))).scalar_one_or_none()
    if not ch:
        ch = Channel(telegram_chat_id=message.chat.id, title=message.chat.title or "")
        session.add(ch)
        await session.flush()
    user = (await session.execute(select(User).where(User.telegram_user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        user = User(telegram_user_id=message.from_user.id, username=message.from_user.username or None,
                    first_name=message.from_user.first_name or None, last_name=message.from_user.last_name or None)
        session.add(user)
        await session.flush()
    ch.owner_user_id = user.id
    await session.commit()
    await message.reply("Проект активирован. Используйте /invite_sales для ссылки.")

@router.message(Command("invite_sales"))
async def invite_sales(message: Message, bot: Bot, session: AsyncSession):
    if message.chat.type not in {"supergroup", "group", "channel"}:
        return await message.reply("Команда доступна только в канале/группе.")
    if not await is_admin(bot, message.chat.id, message.from_user.id):
        return await message.reply("Только админ.")
    token = secrets.token_urlsafe(12)
    ch = (await session.execute(select(Channel).where(Channel.telegram_chat_id == message.chat.id))).scalar_one_or_none()
    if not ch:
        return await message.reply("Сначала /enable_project")
    inv = Invite(channel_id=ch.id, token=token, status="active", created_by_user_id=ch.owner_user_id or 0)
    session.add(inv)
    await session.commit()
    link = await create_start_link(bot, f"inv_{token}", encode=True)
<<<<<<< HEAD
    await message.reply(f"Инвайт для сейлзов: {link}")
=======
    await message.reply(f"Инвайт для сейлзов: {link}")
>>>>>>> d26e15bb748e2dacfacaec01384eaf20197cfb35
