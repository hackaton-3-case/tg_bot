from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


volunteer_profile_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои животные', callback_data='{my_pets}')],
     [InlineKeyboardButton(text='Мои данные', callback_data='{my_data}')],
    [InlineKeyboardButton(text='Добавить животное', callback_data='{add_pet}')]])