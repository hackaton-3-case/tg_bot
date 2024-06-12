import logging
import hashlib
import time
from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from aiogram import Bot

from keyboards import reply_keyboards as reply_keys
from keyboards import inline_keyboards as inline_keys

from data.config import token_tg
import operations
from model import dboperations
from model.dboperations import volunteers_indexes

bot = Bot(token=token_tg)
router = Router()

state_keys = {
    '{main_menu}': reply_keys.main_key,
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
    return state_keys[(await dboperations.get_user_data(tgId))[volunteers_indexes['state']]]


@router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        if (await dboperations.get_user_data(message.from_user.id)) == 'User not exists':
            user_data = await dboperations.get_user_data(0, message.from_user.username)
            if (await dboperations.authorize_user(message.from_user.username, message.from_user.id)) != 'User not exists':
                await message.answer(f'Здравствуйте, {user_data[volunteers_indexes['fio']]}, вы в главном меню!', reply_markup=reply_keys.main_key)
            else:
                await message.answer('Вы не зарегистрированы в системе бота, подайте заявку на нашем сайте /../ и ожидайте предоставления доступа. Если вы меняли юзернейм в Telegram - верните старый и авторизуйтесь в боте или подайте заявку заново.')
        else:
            await message.answer('Вы уже авторизованы в боте, пожалуйста используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer('Неизвестная ошибка, попробуйте еще раз или свяжитесь с администратором.')


@router.message(F.text == 'Взять корм')
async def take_foods_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню выбора откуда...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Реализовать корм')
async def realise_foods_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню введения количества и фотоотчета...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Передать корм')
async def handover_foods_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню ввода количества, айди чела и фотоотчета...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Сдать на склад')
async def put_away_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню ввода количества и фотоотчета...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Карточка волонтёра')
async def volunteer_profile_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await operations.volunteer_profile(message)
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Список точек')
async def points_list_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню крайпака...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text.lower() == 'выход')
async def points_list_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{volunteer_profile_menu}':
        await operations.main_menu(message)
    else:
        await message.answer('Используйте кнопки!')


@router.message()
async def another_message(message: Message):
    state = await dboperations.get_user_data(message.from_user.id)
    if state[volunteers_indexes['state']] == "{waiting_state1}":
        try:
            pass
        except Exception as e:
            logging.info(f'exception in {__name__}: ' + str(e))
            await message.answer('Говно ты ввёл, еще раз')
    else:
        await message.answer(f'Используйте кнопки!', reply_markup=await get_state_keyboard(message.from_user.id))