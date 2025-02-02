#=============================================================================================================
#================================================== Imports ==================================================
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

#============================================================================================================
#=============================================================================================================

class MenuCallBack(CallbackData, prefix="menu"):
    level: int
    menu_name: str
    page: int | None = 1
    product_id: int | None = None

#=============================================================================================================
#=============================================================================================================


def get_user_main_btns(*, level: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        'Ваши термометры ': 'esp_catalog',
        'Добавить термометр': "add_esp",
        'О нас ℹ️': 'about',
        'Пополнить баланс': 'payment',
    }
    for text, menu_name in btns.items():
        if menu_name == "esp_catalog":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(level=1, menu_name=menu_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(level=level, menu_name=menu_name).pack()))
    
    return keyboard.adjust(*sizes).as_markup()

def get_esp_catalog_btns(
        level: int, 
        page: int,
        pagination_btns: dict,
        sizes: tuple[int] = (2, 1),):
    

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад ⏎',
                callback_data=MenuCallBack(level=level-1, menu_name='main_menu').pack()))
    
    keyboard.adjust(*sizes)

    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        page=page + 1).pack()))
            
        elif menu_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        page=page - 1).pack()))

    return keyboard.row(*row).as_markup()