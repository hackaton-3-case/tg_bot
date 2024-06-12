from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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

cat_or_dog_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='кошка'), KeyboardButton(text='собака')],
    [KeyboardButton(text='выход')]],
    resize_keyboard=True
)

male_or_female_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='мальчик'), KeyboardButton(text='девочка')],
    [KeyboardButton(text='выход')]],
    resize_keyboard=True
)

sterialized_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='стерильный'), KeyboardButton(text='не стерильный')],
    [KeyboardButton(text='выход')]],
    resize_keyboard=True
)

moscow_or_mo_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Москва'), KeyboardButton(text='Московская Область')],
    [KeyboardButton(text='выход')]],
    resize_keyboard=True
)