import json
import logging
import time
import re
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart
from aiogram import Bot

from keyboards import reply_keyboards as reply_keys

from tg_bot.data.config import token_tg
import operations
from model import dboperations
from model.dboperations import volunteers_indexes
import tg_bot.src.label.strings as strings

#
# при изменении полномочий сендменю
#

bot = Bot(token=token_tg)
router = Router()

state_keys = {
    '{main_menu}': reply_keys.main_key,
    '{admin_main_menu}': reply_keys.admin_main_key,
    '{admin_menu}': reply_keys.admin_key,
    '{admin_manage_menu}': reply_keys.admin_manage_key,
    '{change_stock_menu}': reply_keys.choose_foods_key,
    '{enter_foods_menu}': reply_keys.exit_key,
    '{volunteer_profile_menu}': reply_keys.exit_key,
    '{register_volunteer_menu:name}': reply_keys.exit_key,
    '{register_volunteer_menu:phone}': reply_keys.exit_key,
    '{register_volunteer_menu:email}': reply_keys.exit_key,
    '{register_volunteer_menu:shortname}': reply_keys.exit_key,
    '{register_volunteer_menu:comment}': reply_keys.exit_key,
    '{register_volunteer_menu:final}': reply_keys.all_good_or_not_key,
    '{add_pet_menu:pet_type}': reply_keys.cat_or_dog_key,
    '{add_pet_menu:sex}': reply_keys.male_or_female_key,
    '{add_pet_menu:sterialized}': reply_keys.sterialized_key,
    '{add_pet_menu:town}': reply_keys.moscow_or_mo_key,
    '{add_pet_menu:district}': reply_keys.exit_key,
    '{add_pet_menu:name}': reply_keys.exit_key
}

temp_pet_data = {
    'district': 'None'
}

temp_volunteer_data = {}
temp_foods_type = ''

food_types = {
    'Сухой корм для собак': 'dogs_dry',
    'Влажный корм для собак': 'dogs_wet',
    'Сухой корм для кошек': 'cats_dry',
    'Влажный корм для кошек': 'cats_wet'
}


def timer(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds")
        return result
    return wrapper


async def get_state_keyboard(tgId):
    """
    :param tgId: The Telegram ID of the user.
    :return: The keyboard layout (likely a list of buttons or commands) corresponding to the user's current state.
    """

    return state_keys[(await dboperations.get_user_data(tgId))[volunteers_indexes['state']]]


def valid_phone_num(phone_num: str) -> bool:
    digits = [str(i) for i in range(10)]
    if phone_num[0] in ['+', *digits]:
        for i in phone_num[1:]:
            if i not in digits:
                return False
    return True


def get_tg_shortname(link):
    if 't.me/' in link:
        return link[link.find('t.me/')+5:]
    elif '@' in link:
        return link[link.find('@')+1:]
    else:
        return False


@router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        if (await dboperations.get_user_data(message.from_user.id)) == 'User not exists':
            if (await dboperations.authorize_user(message.from_user.username, message.from_user.id)) != 'User not exists':
                await operations.main_menu(message)
            else:
                await message.answer(text=strings.start_msg)
        else:
            await message.answer(text=strings.already_register, reply_markup=await get_state_keyboard(message.from_user.id))
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Админское меню')
async def admin_menu_bt(message: Message):
    try:
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == '{admin_main_menu}' and user_data[volunteers_indexes['status']] == 1:
            await operations.admin_menu(message)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Регистрация волонтёра')
async def register_volunteer(message: Message):
    try:
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == '{admin_menu}' and user_data[volunteers_indexes['status']] == 1:
            await dboperations.set_user_state(message.from_user.id, '{register_volunteer_menu:name}')
            await message.answer("Укажите имя и фамилию волонтёра:",
                                          reply_markup=reply_keys.exit_key)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Управление')
async def admin_manage_bt(message: Message):
    try:
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == '{admin_menu}' and user_data[volunteers_indexes['status']] == 1:
            await operations.admin_manage_menu(message)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Изменить содержимое склада')
async def change_stock(message: Message):
    try:
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == '{admin_manage_menu}' and user_data[volunteers_indexes['status']] == 1:
            stock_data = await dboperations.get_user_data(0)
            stock_foods = json.loads(stock_data[volunteers_indexes['foods']])
            await dboperations.set_user_state(message.from_user.id, '{change_stock_menu}')
            await message.answer(f'Сейчас на складе:\n\n{stock_foods['dogs_dry']}кг сухого корма для собак\n{stock_foods['dogs_wet']}кг влажного корма для собак\n{stock_foods['cats_dry']}кг сухого корма для кошек\n{stock_foods['cats_wet']}кг влажного корма для кошек\n\nВыберите какой пункт хотите изменить:', reply_markup=reply_keys.choose_foods_key)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text.in_({'Сухой корм для собак', 'Влажный корм для собак', 'Сухой корм для кошек', 'Влажный корм для кошек'}))
async def what_foods(message: Message):
    try:
        global temp_foods_type
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == '{change_stock_menu}' and user_data[volunteers_indexes['status']] == 1:
            temp_foods_type = message.text
            await dboperations.set_user_state(message.from_user.id, '{enter_foods_menu}')
            await message.answer('Введите новое значение в [кг]:', reply_markup=reply_keys.exit_key)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text.lower().in_({'всё верно', 'нет, хочу изменить'}))
async def final_register_volunteer(message: Message):
    global temp_volunteer_data
    try:
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == '{register_volunteer_menu:final}' and user_data[volunteers_indexes['status']] == 1:
            if message.text == 'Всё верно':
                if type(await dboperations.register_user(temp_volunteer_data['shortname'], temp_volunteer_data['name'], temp_volunteer_data['phone'], temp_volunteer_data['email'], temp_volunteer_data['comment'])) == list:
                    temp_volunteer_data = {}
                    await message.answer("Волонтёр успешно зарегистрирован, теперь он может авторизоваться в боте!")
                    await operations.admin_menu(message)
                else:
                    temp_volunteer_data = {}
                    await message.answer("Произошла ошибка при регистрации волонтёра, попробуйте еще раз")
                    await operations.admin_menu(message)
            else:
                temp_volunteer_data = {}
                await message.answer("Регистрация волонтёра отменена, проведите ёё заново.")
                await operations.admin_menu(message)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Взять корм')
async def take_foods_bt(message: Message):
    try:
        if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
            # todo: implement a system of taking food
            await message.answer('...меню выбора откуда...')
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Реализовать корм')
async def realise_foods_bt(message: Message):
    try:
        if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
            # todo: implement a system of feed sales
            await message.answer('...меню введения количества и фотоотчета...')
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Передать корм')
async def handover_foods_bt(message: Message):
    try:
        if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
            # todo: implement a system of feed transfers
            await message.answer('...меню ввода количества, айди чела и фотоотчета...')
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Сдать на склад')
async def put_away_bt(message: Message):
    try:
        if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
            # todo: implement a system of delivery to the warehouse
            await message.answer('...меню ввода количества и фотоотчета...')
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Карточка волонтёра')
async def volunteer_profile_bt(message: Message):
    try:
        if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
            await operations.volunteer_profile(message)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.callback_query(F.data == '{add_pet}')
async def add_pet(callback: CallbackQuery):
    try:
        user_data = await dboperations.get_user_data(callback.from_user.id)
        if user_data[volunteers_indexes['state']] == "{volunteer_profile_menu}":
            print(await dboperations.set_user_state(callback.from_user.id, '{add_pet_menu:pet_type}'))
            await callback.message.answer("Укажите, какого питомца вы хотите добавить:", reply_markup=reply_keys.cat_or_dog_key)
        else:
            await callback.message.answer('Сообщение больше не актуально, вернитесь в раздел карточки волонтёра.')
    except Exception as e:
        print(str(e))
        await callback.message.answer(text=strings.unknown_error)


@router.message(F.text.lower().in_({'собака', 'кошка'}))
async def cat_or_dog(message: Message):
    try:
        global temp_pet_data
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == "{add_pet_menu:pet_type}":
            temp_pet_data['pet_type'] = message.text
            await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:sex}')
            await message.answer('Укажите пол питомца', reply_markup=reply_keys.male_or_female_key)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text.lower().in_({'мальчик', 'девочка'}))
async def pet_sex(message: Message):
    try:
        global temp_pet_data
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == "{add_pet_menu:sex}":
            temp_pet_data['sex'] = message.text
            await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:sterialized}')
            await message.answer('Стерилен ли ваш питомец?', reply_markup=reply_keys.sterialized_key)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text.lower().in_({'стерилен', 'не стерилен'}))
async def pet_sterialized(message: Message):
    try:
        global temp_pet_data
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == "{add_pet_menu:sterialized}":
            temp_pet_data['sterialized'] = message.text
            await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:town}')
            await message.answer('Питомец проживает в Москве или в МО?', reply_markup=reply_keys.moscow_or_mo_key)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text.lower().in_({'москва', 'московская область'}))
async def moscow_or_mo(message: Message):
    try:
        global temp_pet_data
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == "{add_pet_menu:town}":
            temp_pet_data['town'] = 'Москва' if message.text == 'Москва' else 'МО'
            if message.text == 'Москва':
                await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:district}')
                await message.answer('Введите район Москвы:', reply_markup=reply_keys.exit_key)
            else:
                await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:name}')
                await message.answer('Введите имя питомца:', reply_markup=reply_keys.exit_key)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text == 'Список точек')
async def points_list_bt(message: Message):
    try:
        if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
            # todo: implement a system of nearest points
            await message.answer('...меню крайпака...')
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message(F.text.lower() == 'выход')
async def exit_message(message: Message):
    try:
        global temp_pet_data, temp_volunteer_data
        user_data = (await dboperations.get_user_data(message.from_user.id))
        state = user_data[volunteers_indexes['state']]
        status = user_data[volunteers_indexes['status']]
        if state == '{volunteer_profile_menu}' or state == '{admin_menu}':
            await operations.main_menu(message)
        elif state.startswith('{add_pet_menu'):
            temp_pet_data = {
                'district': 'None'
            }
            await operations.volunteer_profile(message)
        elif state.startswith('{register_volunteer_menu:') and status == 1:
            temp_volunteer_data = {}
            await operations.admin_menu(message)
        elif state in ('{enter_foods_menu}', '{change_stock_menu}'):
            await operations.admin_manage_menu(message)
        else:
            await message.answer('Используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)


@router.message()
async def another_message(message: Message):
    try:
        global temp_pet_data, temp_volunteer_data
        user_data = await dboperations.get_user_data(message.from_user.id)
        if user_data[volunteers_indexes['state']] == "{add_pet_menu:district}":
            try:
                temp_pet_data['district'] = message.text
                await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:name}')
                await message.answer('Введите имя питомца:', reply_markup=reply_keys.exit_key)

            except Exception as e:
                logging.info(f'exception in {__name__}: ' + str(e))
                await message.answer('Попробуйте еще раз')
        elif user_data[volunteers_indexes['state']] == "{add_pet_menu:name}":
            try:
                temp_pet_data['name'] = message.text
                new_pet = await dboperations.new_pet(message.from_user.id, temp_pet_data['pet_type'], temp_pet_data['name'], temp_pet_data['sex'], temp_pet_data['sterialized'], message.from_user.id, temp_pet_data['town'], temp_pet_data['district'])
                if new_pet == 'Done':
                    temp_pet_data = {
                        'district': 'None'
                    }
                    await operations.volunteer_profile(message)
                else:
                    raise Exception
            except Exception as e:
                logging.info(f'exception in {__name__}: ' + str(e))
                await message.answer('Произошла ошибка при регистрации питомца, попробуйте еще раз.')
                temp_pet_data = {
                    'district': 'None'
                }
                await operations.volunteer_profile(message)

        elif user_data[volunteers_indexes['state']] == '{register_volunteer_menu:name}':
            if user_data[volunteers_indexes['status']] == 1:
                temp_volunteer_data['name'] = message.text
                await dboperations.set_user_state(message.from_user.id, '{register_volunteer_menu:phone}')
                await message.answer("Укажите телефон волонтёра:",
                                     reply_markup=reply_keys.exit_key)
            else:
                await message.answer('Используйте кнопки!')
        elif user_data[volunteers_indexes['state']] == '{register_volunteer_menu:phone}':
            if user_data[volunteers_indexes['status']] == 1:
                if valid_phone_num(message.text):
                    temp_volunteer_data['phone'] = message.text
                    await dboperations.set_user_state(message.from_user.id, '{register_volunteer_menu:email}')
                    await message.answer("Укажите электронную почту волонтёра:",
                                         reply_markup=reply_keys.exit_key)
                else:
                    await message.answer("Неверный формат номера, используйте только цифры и символ '+':",
                                         reply_markup=reply_keys.exit_key)
            else:
                await message.answer('Используйте кнопки!')
        elif user_data[volunteers_indexes['state']] == '{register_volunteer_menu:email}':
            if user_data[volunteers_indexes['status']] == 1:
                if re.match(r'[^@]+@[^@]+\.[^@]+', message.text):
                    temp_volunteer_data['email'] = message.text
                    await dboperations.set_user_state(message.from_user.id, '{register_volunteer_menu:shortname}')
                    await message.answer("Укажите ссылку на телеграм волонтёра:",
                                         reply_markup=reply_keys.exit_key)
                else:
                    await message.answer("Неверный формат почты, попробуйте ещё раз:",
                                         reply_markup=reply_keys.exit_key)
            else:
                await message.answer('Используйте кнопки!')
        elif user_data[volunteers_indexes['state']] == '{register_volunteer_menu:shortname}':
            if user_data[volunteers_indexes['status']] == 1:
                if get_tg_shortname(message.text) != False:
                    temp_volunteer_data['shortname'] = get_tg_shortname(message.text)
                    await dboperations.set_user_state(message.from_user.id, '{register_volunteer_menu:comment}')
                    await message.answer("Добавьте комментарий волонтёру, укажите 0 если комментарий не нужен:",
                                         reply_markup=reply_keys.exit_key)
                else:
                    await message.answer("Неверный формат ссылки, попробуйте ещё раз:",
                                         reply_markup=reply_keys.exit_key)
            else:
                await message.answer('Используйте кнопки!')
        elif user_data[volunteers_indexes['state']] == '{register_volunteer_menu:comment}':
            if user_data[volunteers_indexes['status']] == 1:
                temp_volunteer_data['comment'] = message.text
                await dboperations.set_user_state(message.from_user.id, '{register_volunteer_menu:final}')
                await message.answer(f"Информация о новом волонтёре:\n\nИмя - {temp_volunteer_data['name']}\nТелефон - {temp_volunteer_data['phone']}\nЭлектронная почта - {temp_volunteer_data['email']}\nСсылка на телеграм - t.me/{temp_volunteer_data['shortname']}\nКомментарий: {temp_volunteer_data['comment']}\n\nВсё верно?",
                                     reply_markup=reply_keys.all_good_or_not_key)
            else:
                await message.answer('Используйте кнопки!')
        elif user_data[volunteers_indexes['state']] == '{enter_foods_menu}':
            global temp_foods_type
            if user_data[volunteers_indexes['status']] == 1:
                stock_data = await dboperations.get_user_data(0)
                stock_foods = json.loads(stock_data[volunteers_indexes['foods']])
                try:
                    stock_foods[food_types[temp_foods_type]] = float(message.text)
                    stock_foods = json.dumps(stock_foods)
                    change_foods = await dboperations.set_user_foods(0, stock_foods)
                    if change_foods == 'Done':
                        await message.answer(f"Данные изменены!")
                        await operations.admin_manage_menu(message)
                    else:
                        print(change_foods)
                        await message.answer(strings.unknown_error)
                        await operations.admin_manage_menu(message)
                except:
                    await message.answer('Неверное количество корма, введите заново:')
            else:
                await message.answer('Используйте кнопки!')
        else:
            await message.answer(f'Используйте кнопки!', reply_markup=await get_state_keyboard(message.from_user.id))
    except Exception as e:
        print(str(e))
        await message.answer(text=strings.unknown_error)
