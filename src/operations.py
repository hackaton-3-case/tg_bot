import json

from aiogram import types
import asyncio
from model import dboperations
from model.dboperations import volunteers_indexes
from keyboards import reply_keyboards as reply_keys
from keyboards import inline_keyboards as inline_keys


async def main_menu(message):
    """
    :param message: telegram message to reply
    :return: sends the user to the main menu
    """
    user_data, state_change = await asyncio.gather(dboperations.get_user_data(message.from_user.id), dboperations.set_user_state(message.from_user.id, '{main_menu}'))
    if state_change == 'Done':
        if user_data[volunteers_indexes['status']] != 1:
            await dboperations.set_user_state(message.from_user.id, '{main_menu}')
            key = reply_keys.main_key
        else:
            await dboperations.set_user_state(message.from_user.id, '{admin_main_menu}')
            key = reply_keys.admin_main_key
        await message.answer(f'Здравствуйте, {user_data[volunteers_indexes['fio']]}, вы в главном меню!',
                             reply_markup=key)
    else:
        await message.answer(f'Произошла неизвестная ошибка/вы не авторизованы в системе - напишите /start', reply_markup=types.ReplyKeyboardRemove())


async def volunteer_profile(message) -> None:
    """
    :param message: telegram message to reply
    :return: None
    """
    user_data, state_change = await asyncio.gather(dboperations.get_user_data(message.from_user.id),
                                                   dboperations.set_user_state(message.from_user.id, '{volunteer_profile_menu}'))

    # photo = await draw_card(user_data)
    # todo: implement a system of drawing card vol

    if state_change == 'Done':
        pets = json.loads(user_data[volunteers_indexes['pets']])
        foods = json.loads(user_data[volunteers_indexes['foods']])
        realised = json.loads(user_data[volunteers_indexes['realised']])
        await dboperations.set_user_state(message.from_user.id, '{volunteer_profile_menu}')
        await message.answer(f'{user_data[volunteers_indexes['fio']]}, ваша карточка волонтёра:', reply_markup=reply_keys.exit_key)
        await message.answer(f'Айди волонтёра - {user_data[volunteers_indexes['volunteer_id']]}\n\nВы ухаживаете за:\n'
                             f'{pets['cats']} котами\n{pets['dogs']} собаками\n\nВ данный момент у вас на руках:\n'
                             f'{foods['cats_dry']}кг сухого и {foods['cats_wet']}кг влажного корма для котов\n'
                             f'{foods['dogs_dry']}кг сухого и {foods['dogs_wet']}кг влажного корма для собак\n\nВами было реализовано:\n'
                             f'{realised['cats_realised']}кг корма для котов\n'
                             f'{realised['dogs_realised']}кг корма для собак',
                             reply_markup=inline_keys.volunteer_profile_key)
    else:
        await message.answer(f'Произошла неизвестная ошибка/вы не авторизованы в системе - напишите /start',
                             reply_markup=types.ReplyKeyboardRemove())


async def admin_menu(message) -> None:
    state_change = await dboperations.set_user_state(message.from_user.id, '{admin_menu}')
    if state_change == 'Done':
        await message.answer('Админский опционал:', reply_markup=reply_keys.admin_key)
    else:
        await message.answer(f'Произошла неизвестная ошибка/вы не авторизованы в системе - напишите /start',
                             reply_markup=types.ReplyKeyboardRemove())


async def admin_manage_menu(message) -> None:
    state_change = await dboperations.set_user_state(message.from_user.id, '{admin_manage_menu}')
    if state_change == 'Done':
        await message.answer('Раздел управления и статистики:', reply_markup=reply_keys.admin_manage_key)
    else:
        await message.answer(f'Произошла неизвестная ошибка/вы не авторизованы в системе - напишите /start',
                             reply_markup=types.ReplyKeyboardRemove())
