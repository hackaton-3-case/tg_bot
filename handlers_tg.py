import logging
import hashlib
import time
from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from aiogram import Bot

from keyboards import reply_keyboards as keys

from data.config import token_tg
from model import dboperaations
from model.dboperaations import volunteers_indexes

bot = Bot(token=token_tg)
router = Router()

state_keys = {
    '{main_menu}': keys.main_key,
    '{waiting_state1}': types.ReplyKeyboardRemove,
}


def timer(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds")
        return result
    return wrapper


async def get_state_keyboard(tgId):
    return state_keys[(await dboperaations.get_user_data(tgId))[volunteers_indexes['state']]]


@router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        if (await dboperaations.get_user_data(message.from_user.id)) == 'User not exists':
            text = message.text.split()
            if len(text) == 2:
                token = hashlib.md5(text[1].encode()).hexdigest()
                if (await dboperaations.authorize_user(message.from_user.id, token)) == 'Done':
                    user_data = await dboperaations.get_user_data(message.from_user.id)
                    await message.answer(f'Здравствуйте, {user_data[volunteers_indexes['fio']]}, вы в главном меню!', reply_markup=keys.main_key)
                else:
                    await message.answer('Неверный ключ доступа, попробуйте еще раз.')
            else:
                await message.answer('Пожалуйста, воспользуйтесь ссылкой от администратора бота. Если переходя по ней вы видите это сообщение - авторизуйтесь вручную командой /start + ключ_доступа,\nнапример: /start authkey123')
        else:
            await message.answer('Вы уже авторизованы в боте, пожалуйста используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer('Неизвестная ошибка, попробуйте еще раз или свяжитесь с администратором.')


@router.message(F.text == 'Взять корм')
async def take_foods(message: Message):
    if (await dboperaations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню выбора откуда...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Реализовать корм')
async def realise_foods(message: Message):
    if (await dboperaations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню введения количества и фотоотчета...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Передать корм')
async def handover_foods(message: Message):
    if (await dboperaations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню ввода количества, айди чела и фотоотчета...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Сдать на склад')
async def take_foods(message: Message):
    if (await dboperaations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню ввода количества и фотоотчета...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Карточка волонтёра')
async def take_foods(message: Message):
    if (await dboperaations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...карточка + (инлайн) опции модерирования подручных животных...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Список точек')
async def take_foods(message: Message):
    if (await dboperaations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню крайпака...')
    else:
        await message.answer('Используйте кнопки!')


@router.message()
async def another_message(message: Message):
    state = await dboperaations.get_user_data(message.from_user.id)
    if state[volunteers_indexes['state']] == "{waiting_state1}":
        try:
            pass
        except Exception as e:
            logging.info(f'exception in {__name__}: ' + str(e))
            await message.answer('Говно ты ввёл, еще раз')
    else:
        await message.answer(f'Используйте кнопки!', reply_markup=await get_state_keyboard(message.from_user.id))