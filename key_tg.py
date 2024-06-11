from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

import dboperaations


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

first_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='абитуриентам')],
    [KeyboardButton(text='студенту')],
    [KeyboardButton(text='⚙')]],
    resize_keyboard=True, input_field_placeholder="Главное меню:")

first_admin_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='абитуриентам')],
    [KeyboardButton(text='студенту')],
    [KeyboardButton(text='рассылка')],
    [KeyboardButton(text='⚙')]],
    resize_keyboard=True, input_field_placeholder="Главное меню:")

student_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='здесь могла бы быть ваша реклама')],
    [KeyboardButton(text='назад')]],
    resize_keyboard=True, input_field_placeholder=":)")

mailing_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='расписание')],
    [KeyboardButton(text='текст')],
    [KeyboardButton(text='назад')]],
    resize_keyboard=True, input_field_placeholder=":)")

otmena_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='отмена')]],
    resize_keyboard=True, input_field_placeholder=":)")

okey_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅', callback_data='yes'), InlineKeyboardButton(text='❌', callback_data='no')]])

last_okey_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='отправить ✅', callback_data='yes_last'),
     InlineKeyboardButton(text='отменить ❌', callback_data='no_last')]])

abitur_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='о колледже', callback_data='college')],
     [InlineKeyboardButton(text='специальности', callback_data='special')],
    [InlineKeyboardButton(text='общежитие', callback_data='obchej')]])

nazad_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='назад', callback_data='nazad')]
])

last_photo_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='отправить ✅', callback_data='yes_last_photo'),
     InlineKeyboardButton(text='отменить ❌', callback_data='no_last_photo')]])

no_photo = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='продолжить без фото')],
    [KeyboardButton(text='отмена')]],
    resize_keyboard=True)

no_text = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='продолжить без текста')],
    [KeyboardButton(text='отмена')]],
    resize_keyboard=True)

def key_settings(weather, schedule, posts, vk):
    yes_weather = InlineKeyboardButton(text='погода ✅', callback_data='weather_off')
    yes_schedule = InlineKeyboardButton(text='раписание ✅', callback_data='schedule_off')
    yes_post = InlineKeyboardButton(text='новые записи ✅', callback_data='posts_off')

    no_weather = InlineKeyboardButton(text='погода ❌', callback_data='weather_on')
    no_schedule = InlineKeyboardButton(text='раписание ❌', callback_data='schedule_on')
    no_post = InlineKeyboardButton(text='новые записи ❌', callback_data='posts_on')

    add_vk = InlineKeyboardButton(text='привязать вконтакте', callback_data='add_vk')
    if vk == 0:
        if weather == 1:
            if schedule == 1:
                if posts == 1:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [yes_weather], [yes_schedule], [yes_post], [add_vk]
                    ])
                else:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [yes_weather], [yes_schedule], [no_post], [add_vk]
                    ])
            else:
                if posts == 1:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [yes_weather], [no_schedule], [yes_post], [add_vk]
                    ])
                else:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [yes_weather], [no_schedule], [no_post], [add_vk]
                    ])
        else:
            if schedule == 1:
                if posts == 1:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [no_weather], [yes_schedule], [yes_post], [add_vk]
                    ])
                else:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [no_weather], [yes_schedule], [no_post], [add_vk]
                    ])
            else:
                if posts == 1:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [no_weather], [no_schedule], [yes_post], [add_vk]
                    ])
                else:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [no_weather], [no_schedule], [no_post], [add_vk]
                    ])
    else:
        if weather == 1:
            if schedule == 1:
                if posts == 1:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [yes_weather], [yes_schedule], [yes_post]
                    ])
                else:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [yes_weather], [yes_schedule], [no_post]
                    ])
            else:
                if posts == 1:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [yes_weather], [no_schedule], [yes_post],
                    ])
                else:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [yes_weather], [no_schedule], [no_post]
                    ])
        else:
            if schedule == 1:
                if posts == 1:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [no_weather], [yes_schedule], [yes_post]
                    ])
                else:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [no_weather], [yes_schedule], [no_post]
                    ])
            else:
                if posts == 1:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [no_weather], [no_schedule], [yes_post]
                    ])
                else:
                    settings = InlineKeyboardMarkup(inline_keyboard=[
                        [no_weather], [no_schedule], [no_post]
                    ])

    return settings


def what_key(us_id=876545829):
    popa = dboperaations.get_user_data(us_id)
    state, who = popa[1]
    if state == "hello_menu":
        return hello
    if state in ["first_menu", "config_menu"] and who == 0:
        if state == "config_menu":
            cursor.execute(f"UPDATE users SET state = 'first_menu' WHERE us_id = {us_id}")
            conn.commit()
        return first_key
    if state in ["first_menu", "config_menu"] and who == 1:
        if state == "config_menu":
            cursor.execute(f"UPDATE users SET state = 'first_menu' WHERE us_id = {us_id}")
            conn.commit()
        return first_admin_key
    if state == "student_menu":
        return student_key
    if state == "abitur_menu":
        return abitur_key
    if state == "mailing_config":
        return mailing_key
    if state in ["schedule_send", "last_continue"]:
        return otmena_key
