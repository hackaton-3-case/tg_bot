import json

from tg_bot.src.data.config import url
import asyncpg

volunteers_indexes = {
    'volunteer_id': 0,
    'telegram_id': 1,
    'fio': 2,
    'status': 3,
    'state': 4,
    'phone': 5,
    'email': 6,
    'passport_data': 7,
    'pets': 8,
    'foods': 9,
    'realised': 10,
    'telegram_shortname': 11,
    'pet_ids': 12,
    'comment': 13
}

pets_indexes = {
    'pet_id': 0,
    'pet_type': 1,
    'name': 2,
    'town': 3,
    'district': 4,
    'sex': 5,
    'sterialised': 6,
    'volunteer_id': 7
}


async def register_user(shortname, fio, phone, email, comment='', passport_data='нет информации'):
    """
    :param comment: user profile comment
    :param shortname: telegram shortname (link to profile)
    :param fio: full name
    :param phone: phone number
    :param email: email address
    :param passport_data: passport data
    :return: add user to database and welcome to the bot
    """
    try:
        conn = await asyncpg.connect(url)
        json_pets = json.dumps({'cats': 0, 'dogs': 0})
        json_foods = json.dumps({'cats_dry': 0, 'cats_wet': 0, 'dogs_dry': 0, 'dogs_wet': 0})
        json_realised = json.dumps({'cats_realised': 0, 'dogs_realised': 0})
        state = '{not_authorized}'
        pet_ids = '{}'
        await conn.execute(f"INSERT INTO volunteers (telegram_id, fio, status, state, phone, email, passport_data, pets, foods, realised, telegram_shortname, pet_ids, comment) "
                           f"VALUES (0, '{fio}', 0, '{state}', '{phone}', '{email}', '{passport_data}', '{json_pets}', '{json_foods}', '{json_realised}', '{shortname}', '{pet_ids}', '{comment}')")
        await conn.close()
        return [fio, f't.me/{shortname}']
    except Exception as e:
        await conn.close()
        print(f'Exception: {str(e)}')
        return f'Exception: {str(e)}'


async def authorize_user(shortname, tgId):
    """
    :param shortname: telegram shortname (link to profile)
    :param tgId: telegram id (the user's unique number)
    :return: if user is found - 'Done'. else - 'User not exists'
    """
    try:
        conn = await asyncpg.connect(url)
        if len(await conn.fetch(f"SELECT * FROM volunteers WHERE telegram_shortname='{shortname}'")) != 0:
            state = '{main_menu}'
            await conn.execute(f"UPDATE volunteers SET telegram_id={tgId}, state='{state}' WHERE telegram_shortname='{shortname}'")
            await conn.close()
            return 'Done'
        else:
            return 'User not exists'
    except Exception as e:
        await conn.close()
        print(f'Exception: {str(e)}')
        return f'Exception: {str(e)}'


async def get_user_data(tgId, username=None):
    """
    The function returns a coroutine with information about the user
    :param tgId: telegram id (the user's unique number)
    :param username: telegram shortname (link to profile)
    """
    try:
        conn = await asyncpg.connect(url)
        if username is None:
            answer = await conn.fetch(f"SELECT * FROM volunteers WHERE telegram_id={tgId}")
        else:
            answer = await conn.fetch(f"SELECT * FROM volunteers WHERE telegram_shortname='{username}'")
        if len(answer) != 0:
            await conn.close()
            return answer[0]
        else:
            await conn.close()
            return 'User not exists'
    except Exception as e:
        await conn.close()
        return f'Exception: {str(e)}'


async def set_user_state(tgId, new_state):
    """
    The function set new user state
    :param tgId: telegram id (the user's unique number)
    :param new_state: new state of the user
    :return: if user is found - 'Done'. else - 'User not exists'
    """
    try:
        conn = await asyncpg.connect(url)
        answer = await conn.fetch(f'SELECT * FROM volunteers WHERE telegram_id={tgId}')
        if len(answer) != 0:
            await conn.execute(f"UPDATE volunteers SET state = '{new_state}' WHERE telegram_id = {tgId}")
            return 'Done'
        else:
            await conn.close()
            return 'User not exists'
    except Exception as e:
        return f'Exception: {str(e)}'


async def set_user_foods(tgId, foods):
    try:
        conn = await asyncpg.connect(url)
        answer = await conn.fetch(f'SELECT * FROM volunteers WHERE telegram_id={tgId}')
        if len(answer) != 0:
            await conn.execute(f"UPDATE volunteers SET foods = '{foods}' WHERE telegram_id = {tgId}")
            return 'Done'
        else:
            await conn.close()
            return 'User not exists'
    except Exception as e:
        print(e)
        return f'Exception: {str(e)}'


async def new_pet(tgId, pet_type, name, sex, sterialised, volunteer_id, town, district):
    """
    The function create a new pet in database
    :param tgId: telegram id (the user's unique number)
    :param pet_type: cat or dog
    :param name: pet name
    :param sex: pet sex
    :param sterialised: yes or no
    :param volunteer_id: telegram id (the user's unique number)
    :param town: the city where the pet is located
    :param district: district where the pet is located
    """
    try:
        sterialised = True if sterialised == 'стерилен' else False
        conn = await asyncpg.connect(url)
        pets = (await conn.fetch(f"SELECT * FROM volunteers WHERE telegram_id={tgId}"))[0][volunteers_indexes['pets']]
        pets = json.loads(pets)
        pets['cats' if pet_type == 'кошка' else 'dogs'] += 1
        pets = json.dumps(pets)
        pet_id = (await conn.fetch(f"INSERT INTO pets (pet_type, name, town, district, sex, sterialised, volunteer_id) VALUES ('{pet_type}', '{name.capitalize()}', '{town}', '{district.capitalize()}', '{sex}', {sterialised}, {volunteer_id}) RETURNING pet_id"))[0][0]
        await conn.execute(f"UPDATE volunteers SET pet_ids = ARRAY_APPEND(pet_ids, {pet_id}), pets = '{pets}' WHERE telegram_id={tgId}")
        await conn.close()
        return 'Done'
    except Exception as e:
        print(str(e))
        await conn.close()
        return f'Exception: {str(e)}'