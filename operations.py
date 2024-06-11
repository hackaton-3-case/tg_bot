from aiogram import types
import asyncio
import dboperaations
from dboperaations import volunteers_indexes
import key_tg as keys


async def main_menu(message):
    user_data, state_change = await asyncio.gather(dboperaations.get_user_data(message.from_user.id), dboperaations.set_user_state(message.from_user.id, 'main_menu'))
    if state_change == 'Done':
        await message.answer(f'Здравствуйте, {user_data[volunteers_indexes['fio']]}, вы в главном меню!',
                             reply_markup=keys.main_key)
    else:
        print(state_change)
        await message.answer(f'Произошла неизвестная ошибка/ты не зареган - напиши /start', reply_markup=types.ReplyKeyboardRemove())