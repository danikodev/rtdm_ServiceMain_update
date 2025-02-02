#=============================================================================================================
#================================================== Imports ==================================================
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from server_telegram_fold.handlers.user_private import user_private_router

# from middlewares.db import DataBaseSession
# from database.engine import create_db, drop_db, session_maker

# from handlers.user_group import user_group_router
# from handlers.admin_private import admin_router
# from common.bot_cmds_list import private

#=============================================================================================================
#=============================================================================================================

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
bot.my_admins_list = []

dp = Dispatcher()

dp.include_router(user_private_router) 
# dp.include_router(user_group_router)
# dp.include_router(admin_router)

#=============================================================================================================
#=============================================================================================================

async def on_startup(bot):
    # await drop_db()
    # await create_db()
    print("Бот запущен")


async def on_shutdown(bot):
    print('бот лег')

#=============================================================================================================
#=============================================================================================================

async def main():
    dp.startup.register(on_startup) # регистрирует функцию on_startup, которая будет вызываться при запуске
    dp.shutdown.register(on_shutdown) #  регистрирует функцию on_shutdown, которая будет вызываться при завершении работы бота

    # dp.update.middleware(DataBaseSession(session_pool=session_maker)) # создается сессия для работы с базой данных с использованием пула соединений
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())

    

    


    await bot.delete_webhook(drop_pending_updates=True) # Эта строка удаляет вебхук у бота, если он был ранее установлен
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) # Запуск ПУЛИНГА!!! 

#=============================================================================================================
#=============================================================================================================

async def server_telegram_bot_process():
    print('Телеграм сервер запущен')
    await main()
