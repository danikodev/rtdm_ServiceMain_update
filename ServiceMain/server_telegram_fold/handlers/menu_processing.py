#=============================================================================================================
#================================================== Imports ==================================================
from aiogram.types import InputMediaPhoto, InputFile
from server_telegram_fold.database.db_telegram import Paginator
from server_telegram_fold.kbds.inline import get_esp_catalog_btns, get_user_main_btns
from PIL import Image
from io import BytesIO
from server_telegram_fold.database.db_telegram import Database
import math

# from server_telegram_fold.kbds.inline import get_products_btns, get_user_cart, get_user_catalog_btns, get_user_main_btns

# from sqlalchemy.ext.asyncio import AsyncSession
# from database.orm_query import Paginator, orm_delete_from_cart, orm_get_banner, orm_get_categories, orm_get_products, orm_get_user_carts, orm_reduce_product_in_cart
#=============================================================================================================
#=============================================================================================================

db = Database('data/base.db')

#=============================================================================================================
#=============================================================================================================

# def pages(poginator: Paginator):
#     btns = dict()
#     if poginator.has_previous():
#         btns["< Пред."] = "previous"

#     if poginator.has_next():
#         btns["След. >"] = "next"

#     return btns

#=============================================================================================================
#=============================================================================================================

async def get_main_menu(level):
    # Путь к изображению
    media = "AgACAgIAAxkBAAIBHWcvmkDjjuypDXB3wMrVYfej5Gu4AAJ06zEbUfV4SdwHnfH1u_8QAQADAgADbQADNgQ"
    description = "Добро пожаловать!"

    image = InputMediaPhoto(media=media, caption=description)

    # Генерация кнопок меню
    kbds = get_user_main_btns(level=level)

    return image, kbds

# Простой пагинатор


def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns['< Пред.'] = 'previous'
    if paginator.has_next():
        btns['След. >'] = 'next'

    return btns


async def get_esp_catalog(level, page, user_address_telegram):
    # products = await orm_get_products(session, category_id=category~)

    products = db.get_esp_parameters(user_address_telegram)
    # products = f'🌡{products[0]}°С 🌡{products[1]}°С ⚡️{products[2]}V 🟢'
    paginator = Paginator(products, page=page)
    product = paginator.get_page()[0]

    image = InputMediaPhoto(
        media="AgACAgIAAxkBAAIB72dB-Czx5javyt0fZYvYTvWEGEtxAAIq4TEbQtcRSu88Zj0K8dT9AQADAgADbQADNgQ",
        caption=f'<strong>🌡{product[0]}°С 🌡{product[1]}°С ⚡️{product[2]}V 🟢</strong>'
        # caption=f"<strong>{product.name}\
        #         </strong>\n{product.description}\nCтоимость: {round(product.price, 2)}\n\
        #         <strong>Товар {paginator.page} из {paginator.pages}</strong>",
    )

    pagination_btns = pages(paginator)

    kbds = get_esp_catalog_btns(
        level=level,
        page=page,
        pagination_btns=pagination_btns,
    )
    

    return image, kbds


# async def carts(session, level, menu_name, page, user_id, product_id):

#     if menu_name == "delete":
#         await orm_delete_from_cart(session, user_id, product_id)
#         if page > 1: page -=1
#     elif menu_name == "decrement":
#         is_cart = await orm_reduce_product_in_cart(session, user_id, product_id)
#         if page > 1 and not is_cart: page -= 1
#     elif menu_name == "increment":
#         await orm_get_user_carts(session, user_id)

#     carts = await orm_get_user_carts(session, user_id)

#     if not carts:
#         banner = await orm_get_banner(session, "cart")
#         image = InputMediaPhoto(media=banner.image, caption=f"<strong>{banner.description}</strong>")

#         kbds = get_user_cart(
#             level=level,
#             page=None,
#             pogination_btns=None,
#             product_id=None,
#         )

#     else:

#         paginator = Paginator(carts, page=page)

#         cart = paginator.get_page()[0]

#         cart_price = round(cart.quantity*cart.product.price, 2)
#         total_price = round(sum(cart.quantity*cart.product.price for cart in carts), 2)
#         image = InputMediaPhoto(
#             media=cart.product.image,
#             caption=f"<strong>{cart.product.name}</strong>\n{cart.product.price}$ x {cart.quantity} = {cart_price}$\
#                 \nТовар {paginator.page} из {paginator.pages} в карзине. \nОбщая стоимость товаров в корзине {total_price}",
#         )

#         paginator_btns = pages(paginator)

#         kbds = get_user_cart(
#             level=level,
#             page=page,
#             pogination_btns=paginator_btns,
#             product_id=cart.product.id,
#         )
#     return image, kbds


#=============================================================================================================
#=============================================================================================================



# Создаем меню
async def get_menu_content(
    level: int,                     # Уровень погружения
    menu_name: str,                 # Название меню   
    page: int | None = None,
    user_address_telegram: int | None = None,
    # product_id: int | None = None,
):
    

    # если уровень 0 то вернуть главную страницу
    if level == 0:
        return await get_main_menu(level)
    elif level == 1:
        return await get_esp_catalog(level, page, user_address_telegram) # Все тавары
    # elif level == 2:
    #     return await products(session, level, category, page)
    # elif level == 3:
    #     return await carts(session, level, menu_name, page, user_id, product_id)