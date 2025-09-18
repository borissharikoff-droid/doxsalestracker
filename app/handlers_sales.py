from __future__ import annotations
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Channel, ChannelMember, Sale, User

router = Router(name="sales")

async def notify_owner(bot: Bot, channel: Channel, text: str) -> None:
    if channel.owner_user_id:
        try:
            await bot.send_message(chat_id=channel.owner_user_id, text=text)
        except Exception:
            pass

@router.message(Command("add_sale"))
async def add_sale(message: Message, bot: Bot, session: AsyncSession):
    if message.chat.type not in {"supergroup", "group", "channel"}:
        return await message.reply("Добавлять продажи нужно в канале/группе проекта.")
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2:
        return await message.reply("Использование: /add_sale <сумма> [комментарий]")
    try:
        amount = float(parts[1])
    except ValueError:
        return await message.reply("Некорректная сумма.")
    comment = parts[2] if len(parts) > 2 else None
    user = (await session.execute(select(User).where(User.telegram_user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        return await message.reply("Сначала стартуйте бота в ЛС: /start")
    ch = (await session.execute(select(Channel).where(Channel.telegram_chat_id == message.chat.id))).scalar_one_or_none()
    if not ch:
        return await message.reply("Канал не зарегистрирован. Админу: /enable_project")
    membership = (await session.execute(select(ChannelMember).where(ChannelMember.channel_id == ch.id, ChannelMember.user_id == user.id, ChannelMember.role == "sales"))).scalar_one_or_none()
    if not membership:
        return await message.reply("Вы не являетесь сейлзом этого проекта.")
    sale = Sale(channel_id=ch.id, user_id=user.id, amount=amount, comment=comment)
    session.add(sale)
    await session.commit()
    await message.reply("Продажа сохранена.")
    await notify_owner(bot, ch, f"Новая продажа: {amount} от @{message.from_user.username or message.from_user.id}")
