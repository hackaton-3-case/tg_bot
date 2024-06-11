from aiogram import types
import asyncio
from tg_bot.model import dboperaations
from tg_bot.model.dboperaations import volunteers_indexes
from tg_bot.keyboards import reply_keyboards as keys


async def main_menu(message):
    user_data, state_change = await asyncio.gather(dboperaations.get_user_data(message.from_user.id), dboperaations.set_user_state(message.from_user.id, '{main_menu}'))
    if state_change == 'Done':
        await dboperaations.set_user_state(message.from_user.id, '{main_menu}')
        await message.answer(f'Здравствуйте, {user_data[volunteers_indexes['fio']]}, вы в главном меню!',
                             reply_markup=keys.main_key)
    else:
        print(state_change)
        await message.answer(f'Произошла неизвестная ошибка/вы не авторизованы в системе - напишите /start', reply_markup=types.ReplyKeyboardRemove())