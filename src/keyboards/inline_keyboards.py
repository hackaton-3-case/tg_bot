from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

volunteer_profile_key = InlineKeyboardMarkup(inline_keyboard=[
    # todo:  Add function "add_photo" in folder "src/photos_vol"
    # save photos as "tg0123456789"
    # or photos can be saved by link, as they are stored on servers TG

    # if hasn't avatar - default_photo == "tg0"
    [InlineKeyboardButton(text='Добавить фотографию', callback_data='{add_photo_profile}')],
    [InlineKeyboardButton(text='Мои животные', callback_data='{my_pets}')],
     [InlineKeyboardButton(text='Мои данные', callback_data='{my_data}')],
    [InlineKeyboardButton(text='Добавить животное', callback_data='{add_pet}')]])