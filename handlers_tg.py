import asyncio
import logging
import hashlib
import time
from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart
from aiogram import Bot

from keyboards import reply_keyboards as reply_keys
from keyboards import inline_keyboards as inline_keys

from data.config import token_tg
import operations
from model import dboperations
from model.dboperations import volunteers_indexes

bot = Bot(token=token_tg)
router = Router()

state_keys = {
    '{main_menu}': reply_keys.main_key,
    '{volunteer_profile_menu}': reply_keys.exit_key,
    '{add_pet_menu:type}': reply_keys.cat_or_dog_key,
    '{add_pet_menu:sex}': reply_keys.male_or_female_key,
    '{add_pet_menu:sterialized}': reply_keys.sterialized_key,
    '{add_pet_menu:town}': reply_keys.moscow_or_mo_key,
    '{add_pet_menu:district}': reply_keys.exit_key,
    '{add_pet_menu:name}': reply_keys.exit_key
}

temp_data = {
    'district': 'None'
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
    return state_keys[(await dboperations.get_user_data(tgId))[volunteers_indexes['state']]]


@router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        if (await dboperations.get_user_data(message.from_user.id)) == 'User not exists':
            user_data = await dboperations.get_user_data(0, message.from_user.username)
            if (await dboperations.authorize_user(message.from_user.username, message.from_user.id)) != 'User not exists':
                await message.answer(f'Здравствуйте, {user_data[volunteers_indexes['fio']]}, вы в главном меню!', reply_markup=reply_keys.main_key)
            else:
                await message.answer('Вы не зарегистрированы в системе бота, подайте заявку на нашем сайте /../ и ожидайте предоставления доступа. Если вы меняли юзернейм в Telegram - верните старый и авторизуйтесь в боте или подайте заявку заново.')
        else:
            await message.answer('Вы уже авторизованы в боте, пожалуйста используйте кнопки!', reply_markup=await get_state_keyboard(message.from_user.id))
    except Exception as e:
        print(str(e))
        await message.answer('Неизвестная ошибка, попробуйте еще раз или свяжитесь с администратором.')


@router.message(F.text == 'Взять корм')
async def take_foods_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню выбора откуда...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Реализовать корм')
async def realise_foods_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню введения количества и фотоотчета...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Передать корм')
async def handover_foods_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню ввода количества, айди чела и фотоотчета...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Сдать на склад')
async def put_away_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню ввода количества и фотоотчета...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Карточка волонтёра')
async def volunteer_profile_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await operations.volunteer_profile(message)
    else:
        await message.answer('Используйте кнопки!')


@router.callback_query(F.data == '{add_pet}')
async def add_pet(callback: CallbackQuery):
    user_data = await dboperations.get_user_data(callback.from_user.id)
    if user_data[volunteers_indexes['state']] == "{volunteer_profile_menu}":
        print(await dboperations.set_user_state(callback.from_user.id, '{add_pet_menu:type}'))
        await callback.message.answer("Укажите, какого питомца вы хотите добавить:", reply_markup=reply_keys.cat_or_dog_key)
    else:
        await callback.answer('Сообщение больше не актуально, вернитесь в раздел карточки волонтёра.')


@router.message(F.text.lower().in_({'собака', 'кошка'}))
async def cat_or_dog(message: Message):
    global temp_data
    user_data = await dboperations.get_user_data(message.from_user.id)
    if user_data[volunteers_indexes['state']] == "{add_pet_menu:type}":
        temp_data['type'] = message.text
        await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:sex}')
        await message.answer('Укажите пол питомца', reply_markup=reply_keys.male_or_female_key)
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text.lower().in_({'мальчик', 'девочка'}))
async def pet_sex(message: Message):
    global temp_data
    user_data = await dboperations.get_user_data(message.from_user.id)
    if user_data[volunteers_indexes['state']] == "{add_pet_menu:sex}":
        temp_data['sex'] = message.text
        await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:sterialized}')
        await message.answer('Стерилен ли ваш питомец?', reply_markup=reply_keys.sterialized_key)
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text.lower().in_({'стерилен', 'не стерилен'}))
async def pet_sterialized(message: Message):
    global temp_data
    user_data = await dboperations.get_user_data(message.from_user.id)
    if user_data[volunteers_indexes['state']] == "{add_pet_menu:sterialized}":
        temp_data['sterialized'] = message.text
        await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:town}')
        await message.answer('Питомец проживает в Москве или в МО?', reply_markup=reply_keys.moscow_or_mo_key)
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text.lower().in_({'москва', 'московская область'}))
async def moscow_or_mo(message: Message):
    global temp_data
    user_data = await dboperations.get_user_data(message.from_user.id)
    if user_data[volunteers_indexes['state']] == "{add_pet_menu:town}":
        temp_data['town'] = 'Москва' if message.text == 'Москва' else 'МО'
        if message.text == 'Москва':
            await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:district}')
            await message.answer('Введите район Москвы:', reply_markup=reply_keys.exit_key)
        else:
            await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:name}')
            await message.answer('Введите имя питомца:', reply_markup=reply_keys.exit_key)
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text == 'Список точек')
async def points_list_bt(message: Message):
    if (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']] == '{main_menu}':
        await message.answer('...меню крайпака...')
    else:
        await message.answer('Используйте кнопки!')


@router.message(F.text.lower() == 'выход')
async def exit_message(message: Message):
    global temp_data
    state = (await dboperations.get_user_data(message.from_user.id))[volunteers_indexes['state']]
    if state == '{volunteer_profile_menu}':
        await operations.main_menu(message)
    elif state.startswith('{add_pet_menu'):
        temp_data = {
            'district': 'None'
        }
        await operations.volunteer_profile(message)
    else:
        await message.answer('Используйте кнопки!')


@router.message()
async def another_message(message: Message):
    global temp_data
    state = await dboperations.get_user_data(message.from_user.id)
    if state[volunteers_indexes['state']] == "{add_pet_menu:district}":
        try:
            temp_data['district'] = message.text
            await dboperations.set_user_state(message.from_user.id, '{add_pet_menu:name}')
            await message.answer('Введите имя питомца:', reply_markup=reply_keys.exit_key)

        except Exception as e:
            logging.info(f'exception in {__name__}: ' + str(e))
            await message.answer('Попробуйте еще раз')
    elif state[volunteers_indexes['state']] == "{add_pet_menu:name}":
        try:
            temp_data['name'] = message.text
            new_pet = await dboperations.new_pet(message.from_user.id, temp_data['type'], temp_data['name'], temp_data['sex'], temp_data['sterialized'], message.from_user.id, temp_data['town'], temp_data['district'])
            if new_pet == 'Done':
                temp_data = {
                    'district': 'None'
                }
                await operations.volunteer_profile(message)
            else:
                raise Exception
        except Exception as e:
            logging.info(f'exception in {__name__}: ' + str(e))
            await message.answer('Произошла ошибка при регистрации питомца, попробуйте еще раз.')
            temp_data = {
                'district': 'None'
            }
            await operations.volunteer_profile(message)
    else:
        await message.answer(f'Используйте кнопки!', reply_markup=await get_state_keyboard(message.from_user.id))