import json

from aiogram import types
import asyncio
from model import dboperaations
from model.dboperaations import volunteers_indexes
from keyboards import reply_keyboards as reply_keys
from keyboards import inline_keyboards as inline_keys


async def main_menu(message):
    user_data, state_change = await asyncio.gather(dboperaations.get_user_data(message.from_user.id), dboperaations.set_user_state(message.from_user.id, '{main_menu}'))
    if state_change == 'Done':
        await dboperaations.set_user_state(message.from_user.id, '{main_menu}')
        await message.answer(f'Здравствуйте, {user_data[volunteers_indexes['fio']]}, вы в главном меню!',
                             reply_markup=reply_keys.main_key)
    else:
        await message.answer(f'Произошла неизвестная ошибка/вы не авторизованы в системе - напишите /start', reply_markup=types.ReplyKeyboardRemove())


async def volunteer_profile(message):
    user_data, state_change = await asyncio.gather(dboperaations.get_user_data(message.from_user.id),
                                                   dboperaations.set_user_state(message.from_user.id, '{volunteer_profile_menu}'))
    if state_change == 'Done':
        pets = json.loads(user_data[volunteers_indexes['pets']])
        foods = json.loads(user_data[volunteers_indexes['foods']])
        realised = json.loads(user_data[volunteers_indexes['realised']])
        await dboperaations.set_user_state(message.from_user.id, '{volunteer_profile_menu}')
        await message.answer(f'{user_data[volunteers_indexes['fio']]}, ваша карточка волонтёра:', reply_markup=reply_keys.exit_key)
        await message.answer(f'Вы ухаживаете за:\n'
                             f'{pets['cats']} котами\n{pets['dogs']} собаками\n\nВ данный момент у вас на руках:\n'
                             f'{foods['cats_dry']}кг сухого и {foods['cats_wet']}кг влажного корма для котов\n'
                             f'{foods['dogs_dry']}кг сухого и {foods['dogs_wet']}кг влажного корма для собак\n\nВами было реализовано:\n'
                             f'{realised['cats_realised']}кг корма для котов\n'
                             f'{realised['dogs_realised']}кг корма для собак',
                             reply_markup=inline_keys.volunteer_profile_key)
    else:
        await message.answer(f'Произошла неизвестная ошибка/вы не авторизованы в системе - напишите /start',
                             reply_markup=types.ReplyKeyboardRemove())
