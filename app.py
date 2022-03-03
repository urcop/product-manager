import logging

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    logging.info('create database')
    await db.create()
    logging.info('create table users')
    await db.create_table_users()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

