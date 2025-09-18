from __future__ import annotations
from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, ChannelMember, Invite

router = Router(name="sales-join")

@router.message(CommandStart(deep_link=True))
async def start_deeplink(message: Message, command: CommandObject, session: AsyncSession):
    args = command.args or ""
    payload = decode_payload(args)
    if not payload.startswith("inv_"):
        return await message.answer("Добро пожаловать!")
    token = payload[4:]
    inv = (await session.execute(select(Invite).where(Invite.token == token, Invite.status == "active"))).scalar_one_or_none()
    if not inv:
        return await message.answer("Ссылка недействительна.")
    user = (await session.execute(select(User).where(User.telegram_user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        user = User(telegram_user_id=message.from_user.id, username=message.from_user.username or None,
                    first_name=message.from_user.first_name or None, last_name=message.from_user.last_name or None)
        session.add(user)
        await session.flush()
    exists = (await session.execute(select(ChannelMember).where(ChannelMember.channel_id == inv.channel_id, ChannelMember.user_id == user.id))).scalar_one_or_none()
    if not exists:
        session.add(ChannelMember(channel_id=inv.channel_id, user_id=user.id, role="sales"))
    inv.status = "used"
    await session.commit()
    await message.answer("Вы присоединились как сейлз. Админ может назначить вам комиссию.")
