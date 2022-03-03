from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from asyncpg.exceptions import UniqueViolationError

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.add_user(
            fullname=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id=int(message.from_user.id)
        )
        text = (
            f"👋 Добро пожаловать, <b>{message.from_user.full_name}</b>\n",
            "Я бот для приема заявок, нажмите кнопку создать заявку и следуйте инструкциям"
            "Далее наш менеджер свяжется с вами"
        )
        await message.answer("\n".join(text))
    except UniqueViolationError:
        await db.select_user(telegram_id=int(message.from_user.id))
        await message.answer('👋 С возвращением!')
