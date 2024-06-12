import json

import asyncio
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
    'pet_ids': 12
}

pets_indexes = {
    'pet_id': 0,
    'type': 1,
    'name': 2,
    'town': 3,
    'district': 4,
    'sex': 5,
    'sterialised': 6,
    'volunteer_id': 7
}


async def register_user(shortname, fio, phone, email, passport_data='нет информации'):
    try:
        conn = await asyncpg.connect('postgres://postgres:popa123@31.128.37.138:5432/nakormi_telegram_bot')
        json_pets = json.dumps({'cats': 0, 'dogs': 0})
        json_foods = json.dumps({'cats_dry': 0, 'cats_wet': 0, 'dogs_dry': 0, 'dogs_wet': 0})
        json_realised = json.dumps({'cats_realised': 0, 'dogs_realised': 0})
        state = '{not_authorized}'
        pet_ids = '{}'
        await conn.execute(f"INSERT INTO volunteers (telegram_id, fio, status, state, phone, email, passport_data, pets, foods, realised, telegram_shortname, pet_ids) VALUES (0, '{fio}', 0, '{state}', '{phone}', '{email}', '{passport_data}', '{json_pets}', '{json_foods}', '{json_realised}', '{shortname}', '{pet_ids}')")
        await conn.close()
        return [fio, f't.me/{shortname}']
    except Exception as e:
        await conn.close()
        print(f'Exception: {str(e)}')
        return f'Exception: {str(e)}'


async def authorize_user(shortname, tgId):
    try:
        conn = await asyncpg.connect('postgres://postgres:popa123@31.128.37.138:5432/nakormi_telegram_bot')
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
    try:
        conn = await asyncpg.connect('postgres://postgres:popa123@31.128.37.138:5432/nakormi_telegram_bot')
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
    try:
        conn = await asyncpg.connect('postgres://postgres:popa123@31.128.37.138:5432/nakormi_telegram_bot')
        answer = await conn.fetch(f'SELECT * FROM volunteers WHERE telegram_id={tgId}')
        if len(answer) != 0:
            await conn.execute(f"UPDATE volunteers SET state = '{new_state}' WHERE telegram_id = {tgId}")
            return 'Done'
        else:
            await conn.close()
            return 'User not exists'
    except Exception as e:
        return f'Exception: {str(e)}'


async def new_pet(tgId, type, name, sex, sterialised, volunteer_id, town, district):
    try:
        sterialised = True if sterialised == 'стерилен' else False
        conn = await asyncpg.connect('postgres://postgres:popa123@31.128.37.138:5432/nakormi_telegram_bot')
        pets = (await conn.fetch(f"SELECT * FROM volunteers WHERE telegram_id={tgId}"))[0][volunteers_indexes['pets']]
        pets = json.loads(pets)
        pets['cats' if type == 'кошка' else 'dogs'] += 1
        pets = json.dumps(pets)
        pet_id = (await conn.fetch(f"INSERT INTO pets (type, name, town, district, sex, sterialised, volunteer_id) VALUES ('{type}', '{name.capitalize()}', '{town}', '{district.capitalize()}', '{sex}', {sterialised}, {volunteer_id}) RETURNING pet_id"))[0][0]
        await conn.execute(f"UPDATE volunteers SET pet_ids = ARRAY_APPEND(pet_ids, {pet_id}), pets = '{pets}' WHERE telegram_id={tgId}")
        await conn.close()
        return 'Done'
    except Exception as e:
        print(str(e))
        await conn.close()
        return f'Exception: {str(e)}'