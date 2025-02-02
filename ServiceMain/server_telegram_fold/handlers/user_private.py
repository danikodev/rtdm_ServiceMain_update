#=============================================================================================================
#================================================== Imports ==================================================
from aiogram import F, types, Router
from aiogram.filters import CommandStart
from server_telegram_fold.handlers.menu_processing import get_esp_catalog, get_main_menu, get_menu_content
from server_telegram_fold.database.db_telegram import Database
from server_telegram_fold.kbds.inline import MenuCallBack
from aiogram.exceptions import TelegramBadRequest
import asyncio

# from sqlalchemy.ext.asyncio import AsyncSession
# from database.orm_query import (orm_add_to_cart, orm_add_user,)
# from filters.chat_types import ChatTypeFilter
# from handlers.manu_processing import get_menu_content
# from kbds.inline import MenuCallBack, get_callback_btns

#=============================================================================================================
#=============================================================================================================

user_private_router = Router()
db = Database('data/base.db')
# user_private_router.message.filter(ChatTypeFilter(["private"])) # нужно для филтрации сообщений которые будут попадать под дикораторы (только в личных сообщениях)

#=============================================================================================================
#=============================================================================================================

# Отлавливает /start
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    #======================================================
    level = 0
    menu_name = "main"
    user_address_telegram = message.from_user.id
    #======================================================
    if not db.is_user_address_telegram_in_base(user_address_telegram):
        db.add_user_address_telegram_in_base(user_address_telegram)
    #======================================================


    media, reply_markup = await get_main_menu(level) 

    
    # Отдаем пользователю inline меню с фото
    await message.answer_photo(photo = media.media, caption=media.caption, reply_markup=reply_markup)  



# Отлавливаем все колбэки у которых префикс menu (в файле kbds/inline)
@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack):
    #======================================================
    level=callback_data.level
    menu_name=callback_data.menu_name
    page=callback_data.page
    user_address_telegram = callback.from_user.id
    message_id = callback.message.message_id
    #======================================================


    if level == 0: # Главное меню
        media, reply_markup = await get_main_menu(level) 
        await callback.message.edit_media(media=media, reply_markup=reply_markup)
        await callback.answer()

    elif level == 1:# Все тавары
        media, reply_markup =  await get_esp_catalog(level, page, user_address_telegram) 
        await callback.message.edit_media(media=media, reply_markup=reply_markup)
        await callback.answer()
        #======================================================
        db.update_user_telegram_location_data(user_address_telegram, message_id, level, page)
        #======================================================


       
        while True:
            #======================================================
            if not db.is_user_telegram_location_current(user_address_telegram, message_id, level, page):
                break
            #======================================================

            await asyncio.sleep(5)

            new_media, new_reply_markup = await get_esp_catalog(level, page, user_address_telegram)
            # Проверка, изменились ли данные
            if new_media != media or new_reply_markup != reply_markup:
                media, reply_markup = new_media, new_reply_markup
                try:
                    await callback.message.edit_media(media=media, reply_markup=reply_markup)
                except:
                    pass  # Сообщение не изменилось


    

    # sent_message = await message.reply("Hello! This is a message that will be edited.")
    # await bot.edit_message_text("Hello! This message has been edited.", chat_id=sent_message.chat.id, message_id=sent_message.message_id)


    

    

        


