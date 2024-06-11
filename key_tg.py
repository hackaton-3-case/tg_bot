from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


#not used
exit_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='выход')]],
    resize_keyboard=True
)

main_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Взять корм'), KeyboardButton(text='Реализовать корм'), KeyboardButton(text='Передать корм')],
    [KeyboardButton(text='Сдать на склад')],
    [KeyboardButton(text='Карточка волонтёра'), KeyboardButton(text='Список точек')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Главное меню:")