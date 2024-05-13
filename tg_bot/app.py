import sys
import asyncio
import os

"""This file is responsible for all bot commands."""

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from middlewares.db import DataBaseSession

from database.engine import create_db, drop_db, session_maker

from handlers.user_private import user_private_router
from common.bot_cmds_list import private


#ALLOWED_UPDATES = [ 'message', 'edited_message', 'inline query', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()

dp.include_router(user_private_router)

async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()
    
    await create_db()

async def on_shutdown(bot):
    print('бот лёг')

  
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())