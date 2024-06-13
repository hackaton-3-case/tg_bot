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

admin_main_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Взять корм'), KeyboardButton(text='Реализовать корм'), KeyboardButton(text='Передать корм')],
    [KeyboardButton(text='Сдать на склад')],
    [KeyboardButton(text='Карточка волонтёра'), KeyboardButton(text='Список точек'), KeyboardButton(text='Админское меню')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Главное меню:"
)

admin_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назначить админа точки'), KeyboardButton(text='Добавление точки')],
    [KeyboardButton(text='Назначить старшего волонтёра'), KeyboardButton(text='Назначить админа бота')],
    [KeyboardButton(text='Регистрация волонтёра'), KeyboardButton(text='Статистика')],
    [KeyboardButton(text='выход')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Админское меню:"
)

all_good_or_not_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Всё верно'), KeyboardButton(text='Нет, хочу изменить')]],
    resize_keyboard=True
)

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
    [KeyboardButton(text='стерилен'), KeyboardButton(text='не стерилен')],
    [KeyboardButton(text='выход')]],
    resize_keyboard=True
)

moscow_or_mo_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Москва'), KeyboardButton(text='Московская Область')],
    [KeyboardButton(text='выход')]],
    resize_keyboard=True
)