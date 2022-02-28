from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = (
        f"👋 Добро пожаловать, <b>{message.from_user.full_name}</b>\n",
        "Я бот для приема заявок, нажмите кнопку создать заявку и следуйте инструкциям"
        "Далее наш менеджер свяжется с вами"
    )
    await message.answer("\n".join(text))
