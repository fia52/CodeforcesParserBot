import threading

from aiogram import executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, HOST, USER, PASSWORD, DB_NAME
from bd_funcs import BotBD

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
bot_bd = BotBD(HOST, USER, PASSWORD, DB_NAME)


if __name__ == "__main__":
    from handlers import register_main_handlers

    register_main_handlers(dp)
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=threading.Thread(target=bot_bd.autoupdater).start(),
    )
