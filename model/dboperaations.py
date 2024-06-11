import json
import hashlib
import asyncpg
import string, secrets

volunteers_indexes = {
    'volunteer_id': 0,
    'telegram_id': 1,
    'fio': 2,
    'status': 3,
    'state': 4,
    'phone': 5,
    'email': 6,
    'passport_data': 7,
    'auth_key': 8,
    'pets': 9,
    'foods': 10,
    'realised': 11
}

async def register_user(fio, phone, email, passport_data):
    try:
        conn = await asyncpg.connect('postgres://postgres:popa123@31.128.37.138:5432/nakormi_telegram_bot')
        auth_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(12))
        auth_key_hashed = hashlib.md5(auth_key.encode()).hexdigest()
        print(await conn.fetch(f"SELECT * FROM volunteers WHERE auth_key='{auth_key}'"))
        while len(await conn.fetch(f"SELECT * FROM volunteers WHERE auth_key='{auth_key_hashed}'")) != 0:
            auth_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(12))
            auth_key_hashed = hashlib.md5(auth_key.encode()).hexdigest()
        json_pets = json.dumps({'cats': 0, 'dogs': 0})
        json_foods = json.dumps({'cats_dry': 0, 'cats_wet': 0, 'dogs_dry': 0, 'dogs_wet': 0})
        json_realised = json.dumps({'cats_realised': 0, 'dogs_realised': 0})
        state = '{not_authorized}'
        await conn.execute(f"INSERT INTO volunteers (telegram_id, fio, status, state, phone, email, passport_data, auth_key, pets, foods, realised) VALUES (0, '{fio}', 0, '{state}', '{phone}', '{email}', '{passport_data}', '{auth_key_hashed}', '{json_pets}', '{json_foods}', '{json_realised}')")
        await conn.close()
        return [fio, auth_key]
    except Exception as e:
        await conn.close()
        print(f'Exception: {str(e)}')
        return f'Exception: {str(e)}'


async def authorize_user(tgId, auth_key_hashed):
    try:
        conn = await asyncpg.connect('postgres://postgres:popa123@31.128.37.138:5432/nakormi_telegram_bot')
        if len(await conn.fetch(f"SELECT * FROM volunteers WHERE auth_key='{auth_key_hashed}'")) != 0:
            state = '{main_menu}'
            await conn.execute(f"UPDATE volunteers SET telegram_id={tgId}, state='{state}', auth_key='0' WHERE auth_key='{auth_key_hashed}'")
            await conn.close()
            return 'Done'
        else:
            return 'Invalid token'
    except Exception as e:
        await conn.close()
        print(f'Exception: {str(e)}')
        return f'Exception: {str(e)}'


async def get_user_data(tgId):
    try:
        conn = await asyncpg.connect('postgres://postgres:popa123@31.128.37.138:5432/nakormi_telegram_bot')
        answer = await conn.fetch(f"SELECT * FROM volunteers WHERE telegram_id={tgId}")
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
