import asyncio
import logging
import hashlib
import time
from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.filters.command import Command, CommandStart
from aiogram import Bot
from aiogram.types import FSInputFile, InputMediaDocument, InputMediaPhoto

import key_tg as keys
from aiogram.methods import send_message, send_document

from config import token_tg
import dboperaations, operations
from dboperaations import volunteers_indexes

bot = Bot(token=token_tg)
router = Router()

state_keys = {
    '{main_menu}': keys.main_key,
    'money_enter_menu': types.ReplyKeyboardRemove,
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
    return state_keys[(await dboperaations.get_user_data(tgId))[volunteers_indexes['state']]]


@router.message(CommandStart())
@timer
async def cmd_start(message: Message):
    try:
        if (await dboperaations.get_user_data(message.from_user.id)) == 'User not exists':
            text = message.text.split()
            if len(text) == 2:
                token = hashlib.md5(text[1].encode()).hexdigest()
                if (await dboperaations.authorize_user(message.from_user.id, token)) == 'Done':
                    user_data = await dboperaations.get_user_data(message.from_user.id)
                    await message.answer(f'Здравствуйте, {user_data[volunteers_indexes['fio']]}, вы в главном меню!', reply_markup=keys.main_key)
                else:
                    await message.answer('Неверный ключ доступа, попробуйте еще раз.')
            else:
                await message.answer('Пожалуйста, воспользуйтесь ссылкой от администратора бота. Если переходя по ней вы видите это сообщение - авторизуйтесь вручную командой /start + ключ_доступа,\nнапример: /start authkey123')
        else:
            await message.answer('Вы уже авторизованы в боте, пожалуйста используйте кнопки!')
    except Exception as e:
        print(str(e))
        await message.answer('Неизвестная ошибка, попробуйте еще раз или свяжитесь с администратором.')


@router.message()
@timer
async def another_message(message: Message):
    state = await dboperaations.get_user_data(message.from_user.id)
    if state[volunteers_indexes['state']] == "money_enter_menu":
        try:
            if int(message.text) > 2147483647:
                await message.answer('Дохера просишь, откатывай')
            else:
                await dboperaations.set_user_balance(message.from_user.id, int(message.text))
                await operations.main_menu(message)
        except Exception as e:
            logging.info(f'exception in {__name__}: ' + str(e))
            await message.answer('Говно ты ввёл, еще раз')
    else:
        await message.answer(f'Используй кнопки чертила', reply_markup=await get_state_keyboard(message.from_user.id))





'''@router.message(Command("m", "me"))
async def menu(message: Message):
    await operations.main_menu(message)


@router.message(F.text.lower().in_({'100$', '1.000.000$', 'другое'}))
async def student(message: Message):
    user_id = message.from_user.id
    if '00' in message.text:
        await dboperaations.set_user_balance(user_id, message.text.replace('$', '').replace('.', ''))
        await operations.main_menu(message)
    else:
        await asyncio.gather(dboperaations.set_user_state(user_id, 'money_enter_menu'), send_msg(message, 'Введи скока хочешь: ', reply_markup=types.ReplyKeyboardRemove()))


@router.message(F.text.lower() == 'popka')
@timer
async def popka(message: Message):
    if (await dboperaations.get_user_data(message.from_user.id))[1] == 'main_menu':
        await asyncio.gather(dboperaations.set_user_balance(message.from_user.id, (await dboperaations.get_user_data(message.from_user.id))[2] + 1))
        await message.answer('Popka is all good!')
    else:
        await message.answer('Используй кнопки чертила!')


@router.message()
@timer
async def another_message(message: Message):
    state = await dboperaations.get_user_data(message.from_user.id)
    if state[1] == "money_enter_menu":
        try:
            if int(message.text) > 2147483647:
                await message.answer('Дохера просишь, откатывай')
            else:
                await dboperaations.set_user_balance(message.from_user.id, int(message.text))
                await operations.main_menu(message)
        except Exception as e:
            logging.info(f'exception in {__name__}: ' + str(e))
            await message.answer('Говно ты ввёл, еще раз')
    else:
        await message.answer(f'Используй кнопки чертила', reply_markup=await get_state_keyboard(message.from_user.id))


async def send_msg(message, text, reply_markup=None):
    await message.answer(text, reply_markup=reply_markup)


@router.message(F.text.lower() == 'студенту')
async def student_info(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user_data = cursor.fetchone()
    if user_data[6] == "first_menu":
        cursor.execute(f"UPDATE users SET state = 'student_menu' WHERE tg_id = {tg_id}")
        conn.commit()
        await message.answer('Привет студент!', reply_markup=keys.student_key)
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.message(F.text.lower() == 'абитуриентам')
async def abitur_info(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user_data = cursor.fetchone()
    if user_data[6] == "first_menu":
        await message.answer("Привет, я абитурик, могу провести небольшую экскурсию по нашему колледжу!", reply_markup=keys.abitur_key)
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.callback_query(F.data == 'college')
async def info(callback: CallbackQuery):
    await callback.message.edit_text(text="Информация о колледже", reply_markup=keys.nazad_key)


@router.callback_query(F.data == 'nazad')
async def info(callback: CallbackQuery):
    await callback.message.edit_text("Привет, я абитурик, могу провести небольшую экскурсию по нашему колледжу!", reply_markup=keys.abitur_key)

@router.callback_query(F.data == 'special')
async def spec(callback: CallbackQuery):
    await callback.message.edit_text("Специальности колледжа",reply_markup=keys.nazad_key)

@router.callback_query(F.data == 'obchej')
async def spec(callback: CallbackQuery):
    await callback.message.edit_text("Информация об общежитии",reply_markup=keys.nazad_key)

@router.message(F.text.lower() == 'рассылка')
async def mailing(message: Message):
    print(message)
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user_data = cursor.fetchone()
    if user_data[6] == "first_menu" and user_data[5] == 1:
        cursor.execute(f"UPDATE users SET state = 'mailing_config' WHERE tg_id = {tg_id}")
        conn.commit()
        await message.answer('Что вы хотите разослать?', reply_markup=keys.mailing_key)
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.message(F.text.lower() == 'расписание')
async def schedule_send(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user_data = cursor.fetchone()
    if user_data[6] == "mailing_config":
        cursor.execute(f"UPDATE users SET state = 'schedule_send' WHERE tg_id = {tg_id}")
        cursor.execute(f"INSERT INTO mailing_sending (id_creator, done, send) "
                       f"VALUES ((SELECT us_id FROM users WHERE tg_id = {tg_id}), 0, 0)")
        conn.commit()
        await message.answer('Отправьте файлы, которые необходимо разослать', reply_markup=keys.otmena_key)
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.message(F.text.lower() == 'отмена')
async def otmena(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user_data = cursor.fetchone()
    if user_data[6] in ["schedule_send", "last_continue", "add_text", "text_send", "add_text_photo", "mailing_config"]:
        cursor.execute(f"UPDATE users SET state = 'mailing_config' WHERE tg_id = {tg_id}")
        cursor.execute(
            f"DELETE FROM mailing_sending WHERE id_creator = (SELECT us_id "
            f"FROM users WHERE tg_id = {tg_id}) and send = 0")
        conn.commit()
        await message.answer('Выберите, что хотите отправить!', reply_markup=keys.mailing_key)
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.callback_query(F.data == 'yes')
async def yes(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "schedule_send":
        cursor.execute(f"UPDATE users SET state = 'add_text' WHERE tg_id = {tg_id}")
        conn.commit()
        await callback.message.delete()
        await callback.message.answer("Напишите текст, который хотите добавить")
    else:
        cursor.execute(f"SELECT state, id_type, us_id FROM users WHERE tg_id = {tg_id}")
        data = cursor.fetchone()
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()
        await callback.message.answer("Используйте кнопки!", reply_markup=keys.what_key(data[0], data[1], data[2]))


@router.callback_query(F.data == 'no')
async def no(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "schedule_send":
        try:
            cursor.execute(f"UPDATE mailing_sending SET done = 1 "
                           f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and done = 0")
            cursor.execute(f"UPDATE users SET state = 'last_continue' WHERE tg_id = {tg_id}")
            conn.commit()
            wea = await ws.weather()
            docs = []
            cursor.execute(f"SELECT * FROM mailing_sending "
                           f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and send = 0")
            data = cursor.fetchone()
            text = wea + "\n(ЕСЛИ ВКЛЮЧЕНА РАССЫЛКА ПОГОДЫ)"

            document = FSInputFile(path=f"{data[3]}")

            document1 = InputMediaDocument(media=FSInputFile(f"{data[3]}"), caption=text)
            document2 = InputMediaDocument(media=FSInputFile(f"{data[5]}"))
            document3 = InputMediaDocument(media=FSInputFile(f"{data[7]}"))

            docs.append(document1)

            if data[5] is not None:
                docs.append(document2)
            if data[7] is not None:
                docs.append(document3)

            if data[5] is None:
                await callback.message.delete()
                await callback.message.answer('Вот что будет отравлено:')
                await bot.send_document(chat_id=callback.message.chat.id, document=document, caption=text)
                await callback.message.answer("Подтвердите рассылку:", reply_markup=keys.last_okey_key)

            elif data[5] is not None:
                await callback.message.delete()
                await callback.message.answer('Вот что будет отравлено:')
                await bot.send_media_group(callback.message.chat.id, media=docs)
                await callback.message.answer("Подтвердите рассылку:", reply_markup=keys.last_okey_key)
        except Exception as E:
            print(E)
            await callback.answer('Чего-то мне плохо... Попробуй еще раз!')
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()
        await callback.message.answer("Используйте кнопки!")


@router.callback_query(F.data == 'yes_last_photo')
async def yes_last(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "last_continue_photo":
        cursor.execute(f"UPDATE users SET state = 'mailing_config' WHERE tg_id = {tg_id}")
        conn.commit()
        cursor.execute(f"SELECT id_send FROM mailing_sending "
                       f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and send = 0")
        id_send = cursor.fetchone()[0]
        cursor.execute(f"UPDATE mailing_sending SET send = 1 "
                       f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and send = 0")
        conn.commit()

        await callback.message.edit_text("Запускаю рассылку...")
        await mailing_send(id_send, 2, callback, "photo")
    else:
        cursor.execute(f"SELECT state, id_type, us_id FROM users WHERE tg_id = {tg_id}")
        data = cursor.fetchone()
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()
        await callback.message.answer("Используйте кнопки!", reply_markup=keys.what_key(data[0], data[1], data[2]))


@router.callback_query(F.data == 'yes_last')
async def yes_last(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "last_continue":
        cursor.execute(f"UPDATE users SET state = 'mailing_config' WHERE tg_id = {tg_id}")
        conn.commit()
        cursor.execute(f"SELECT id_send FROM mailing_sending "
                       f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and send = 0")
        id_send = cursor.fetchone()[0]
        cursor.execute(f"UPDATE mailing_sending SET send = 1 "
                       f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and send = 0")
        conn.commit()

        await callback.message.edit_text("Запускаю рассылку...")
        await mailing_send(id_send, 2, callback, "doc")
    else:
        cursor.execute(f"SELECT state, id_type, us_id FROM users WHERE tg_id = {tg_id}")
        data = cursor.fetchone()
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()
        await callback.message.answer("Используйте кнопки!", reply_markup=keys.what_key(data[0], data[1], data[2]))


@router.callback_query(F.data == 'no_last_photo')
async def no_last(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    cursor.execute(f"SELECT state, id_type, us_id FROM users WHERE tg_id = {tg_id}")
    data = cursor.fetchone()
    if state == "last_continue_photo":
        cursor.execute(f"UPDATE users SET state = 'mailing_config' WHERE tg_id = {tg_id}")
        conn.commit()
        cursor.execute(f"DELETE FROM mailing_sending "
                       f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and send = 0")
        conn.commit()
        await callback.message.delete()
        await callback.message.answer("Выберите, что хотите разослать", reply_markup=keys.what_key(data[0], data[1], data[2]))
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()
        await callback.message.answer("Используйте кнопки!", reply_markup=keys.what_key(data[0], data[1], data[2]))


@router.callback_query(F.data == 'no_last')
async def no_last(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    cursor.execute(f"SELECT state, id_type, us_id FROM users WHERE tg_id = {tg_id}")
    data = cursor.fetchone()
    if state == "last_continue":
        cursor.execute(f"UPDATE users SET state = 'mailing_config' WHERE tg_id = {tg_id}")
        conn.commit()
        cursor.execute(f"DELETE FROM mailing_sending "
                       f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and send = 0")
        conn.commit()
        await callback.message.delete()
        await callback.message.answer("Выберите, что хотите разослать", reply_markup=keys.what_key(data[0], data[1], data[2]))
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()
        await callback.message.answer("Используйте кнопки!", reply_markup=keys.what_key(data[0], data[1], data[2]))


@router.message(F.text.lower() == 'назад')
async def back(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user_data = cursor.fetchone()

    if user_data[6] in ["student_menu", "abitur_menu", "mailing_config", "text_send"]:
        cursor.execute(f"UPDATE users SET state = 'first_menu' WHERE tg_id = {tg_id}")
        conn.commit()
        await message.answer('Главное меню', reply_markup=keys.first_key if user_data[5] == 0 else keys.first_admin_key)
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.message(F.text == '⚙')
async def setting(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user_data = cursor.fetchone()
    if user_data[6] == "first_menu":
        cursor.execute(f"SELECT * FROM mailing_config WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
        user_data_conf = cursor.fetchone()
        cursor.execute(f"SELECT vk_id FROM users WHERE tg_id = {tg_id}")
        vk_id = cursor.fetchone()[0]
        if vk_id != 0:
            vk_id = 1

        await message.answer('⚙ Настройки',
                             reply_markup=keys.key_settings(user_data_conf[1], user_data_conf[2], user_data_conf[3],
                                                           vk_id))
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.message(F.text.lower() == 'текст')
async def text_send(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user_data = cursor.fetchone()
    if user_data[6] == "mailing_config":
        cursor.execute(f"UPDATE users SET state = 'text_send' WHERE tg_id = {tg_id}")
        cursor.execute(f"INSERT INTO mailing_sending (id_creator, done, send) "
                       f"VALUES ((SELECT us_id FROM users WHERE tg_id = {tg_id}), 0, 0)")
        conn.commit()
        await message.answer('Вместе с текстом вы можете отправить фото', reply_markup=keys.no_photo)
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.callback_query(F.data == 'weather_off')
async def weather_off(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(
        f"UPDATE mailing_config SET weather = 0 WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
    conn.commit()
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "first_menu":
        cursor.execute(f"SELECT * FROM mailing_config WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
        user_data = cursor.fetchone()
        cursor.execute(f"SELECT vk_id FROM users WHERE tg_id = {tg_id}")
        vk_id = cursor.fetchone()[0]
        if vk_id != 0:
            vk_id = 1
        await callback.answer('❌ Рассылка погоды отключена')
        await callback.message.edit_reply_markup(
            reply_markup=keys.key_settings(user_data[1], user_data[2], user_data[3], vk_id))
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()


@router.callback_query(F.data == 'weather_on')
async def weather_on(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(
        f"UPDATE mailing_config SET weather = 1 WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
    conn.commit()
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "first_menu":
        cursor.execute(f"SELECT * FROM mailing_config WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
        user_data = cursor.fetchone()
        cursor.execute(f"SELECT vk_id FROM users WHERE tg_id = {tg_id}")
        vk_id = cursor.fetchone()[0]
        if vk_id != 0:
            vk_id = 1
        await callback.answer('✅ Рассылка погоды включена')
        await callback.message.edit_reply_markup(
            reply_markup=keys.key_settings(user_data[1], user_data[2], user_data[3], vk_id))
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()


@router.callback_query(F.data == 'schedule_off')
async def schedule_off(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(
        f"UPDATE mailing_config SET schedule = 0 WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
    conn.commit()
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "first_menu":
        cursor.execute(f"SELECT * FROM mailing_config WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
        user_data = cursor.fetchone()
        cursor.execute(f"SELECT vk_id FROM users WHERE tg_id = {tg_id}")
        vk_id = cursor.fetchone()[0]
        if vk_id != 0:
            vk_id = 1

        await callback.answer('❌ Рассылка расписания отключена')
        await callback.message.edit_reply_markup(
            reply_markup=keys.key_settings(user_data[1], user_data[2], user_data[3], vk_id))
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()


@router.callback_query(F.data == 'schedule_on')
async def schedule_on(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(
        f"UPDATE mailing_config SET schedule = 1 WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
    conn.commit()
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "first_menu":
        cursor.execute(f"SELECT * FROM mailing_config WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
        user_data = cursor.fetchone()
        cursor.execute(f"SELECT vk_id FROM users WHERE tg_id = {tg_id}")
        vk_id = cursor.fetchone()[0]
        if vk_id != 0:
            vk_id = 1

        await callback.answer('✅ Рассылка расписания включена')
        await callback.message.edit_reply_markup(
            reply_markup=keys.key_settings(user_data[1], user_data[2], user_data[3], vk_id))
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()


@router.callback_query(F.data == 'posts_off')
async def posts_off(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"UPDATE mailing_config SET posts = 0 WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
    conn.commit()
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "first_menu":
        cursor.execute(f"SELECT * FROM mailing_config WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
        user_data = cursor.fetchone()
        cursor.execute(f"SELECT vk_id FROM users WHERE tg_id = {tg_id}")
        vk_id = cursor.fetchone()[0]
        if vk_id != 0:
            vk_id = 1

        await callback.answer('❌ Рассылка новых записей отключена')
        await callback.message.edit_reply_markup(
            reply_markup=keys.key_settings(user_data[1], user_data[2], user_data[3], vk_id))
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()


@router.callback_query(F.data == 'posts_on')
async def posts_on(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"UPDATE mailing_config SET posts = 1 WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
    conn.commit()
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "first_menu":
        cursor.execute(f"SELECT * FROM mailing_config WHERE us_id = (SELECT us_id FROM users WHERE tg_id = {tg_id})")
        user_data = cursor.fetchone()
        cursor.execute(f"SELECT vk_id FROM users WHERE tg_id = {tg_id}")
        vk_id = cursor.fetchone()[0]
        if vk_id != 0:
            vk_id = 1

        await callback.answer('✅ Рассылка новых записей включена')
        await callback.message.edit_reply_markup(
            reply_markup=keys.key_settings(user_data[1], user_data[2], user_data[3], vk_id))
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()


@router.message(F.text.lower() == 'привязать')
async def error_value(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    us_data = cursor.fetchone()
    cursor.execute(f"SELECT * FROM sync WHERE us_id = {us_data[0]}")
    value = cursor.fetchall()
    if us_data[1] == 0:
        if len(value) == 0:
            cursor.execute(f"INSERT INTO sync (us_id, code) VALUES ({us_data[0]}, 'tg{tg_id}')")
            conn.commit()
            await message.answer(
                f'Для привязки используйте команду:\nпривязать vk12345\n(Вместо 12345 ваш секретный код)')
        else:
            await message.answer(
                f'Для привязки используйте команду:\nпривязать vk12345\n(Вместо 12345 ваш секретный код)')
    else:
        await message.answer(f'У вас уже все привязано)')


@router.callback_query(F.data == 'yes_sync')
async def yes_sync(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"SELECT us_id FROM users WHERE tg_id = {tg_id}")
    us_id = cursor.fetchone()[0]
    cursor.execute(f"SELECT vk_id FROM sync_yes WHERE tg_id = {tg_id}")
    vk_id = cursor.fetchone()[0]
    cursor.execute(f"SELECT us_id FROM users WHERE vk_id = {vk_id}")
    us_vk_id = cursor.fetchone()[0]
    cursor.execute(f"UPDATE mailing_sending SET id_creator = {us_vk_id} WHERE id_creator = {us_id}")
    cursor.execute(f"DELETE FROM sync_yes WHERE tg_id = {tg_id} or vk_id = {vk_id}")
    cursor.execute(f"DELETE FROM sync WHERE us_id = {us_id} or us_id = {us_vk_id}")
    cursor.execute(f"DELETE FROM mailing_config WHERE us_id = {us_id}")
    cursor.execute(f"DELETE FROM users WHERE tg_id = {tg_id}")
    cursor.execute(f"UPDATE users SET tg_id = {tg_id} WHERE us_id = {us_vk_id}")
    conn.commit()
    await callback.message.delete()
    await callback.message.answer(text="Успешно")


@router.callback_query(F.data == 'no_sync')
async def yes_sync(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cursor.execute(f"SELECT vk_id FROM sync_yes WHERE tg_id = {tg_id}")
    vk_id = cursor.fetchone()[0]
    cursor.execute(f"DELETE FROM sync_yes WHERE tg_id = {tg_id} or vk_id = {vk_id}")
    conn.commit()
    await callback.message.delete()
    await callback.message.answer(text="Успешно")


@router.callback_query(F.data == 'add_vk')
async def posts_on(callback: CallbackQuery):
    tg_id = callback.from_user.id

    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    cursor.execute(f"SELECT us_id FROM users WHERE tg_id = {tg_id}")
    us_id = cursor.fetchone()[0]
    cursor.execute(f"SELECT vk_id FROM users WHERE tg_id = {tg_id}")
    vk_id = cursor.fetchone()[0]

    if vk_id == 0:
        if state == "first_menu":
            cursor.execute(f"SELECT * FROM sync WHERE us_id = {us_id}")
            value = cursor.fetchall()
            if len(value) == 0:
                cursor.execute(f"INSERT INTO sync (us_id, code) VALUES ({us_id}, 'tg{tg_id}')")
                conn.commit()
                await callback.message.answer(f'Ваш секретный tg код - `tg{tg_id}`\n\n'
                                              f'Для привязки тг к вк используйте команду:\n`привязать tg{tg_id}` в вк',
                                              parse_mode='MarkDown')
            else:
                await callback.message.answer(f'Ваш секретный tg код - `tg{tg_id}`\n\n'
                                              f'Для привязки тг к вк используйте команду:\n`привязать tg{tg_id}` в вк',
                                              parse_mode='MarkDown')
        else:
            await callback.answer('❌ Сообщение больше не актуально')
            await callback.message.delete()
    else:
        await callback.answer('❌ Сообщение больше не актуально')
        await callback.message.delete()


@router.message(F.text.lower().startswith('привязать'))
async def sync_vk(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT vk_id FROM users WHERE tg_id = {tg_id}")
    vk_id = cursor.fetchone()[0]
    if vk_id == 0:
        text = message.text
        text = text.split(" ")
        soc = str(text[1])
        soc = soc[0:2]
        if soc == "tg":
            await message.reply("Ошибка!\nДанный код используется для привязки тг к вк.")
        else:
            try:
                cursor.execute(f"SELECT us_id FROM sync WHERE code = '{text[1]}'")
                us_id = cursor.fetchone()[0]
                cursor.execute(f"SELECT vk_id FROM users WHERE us_id = {us_id}")
                vk_id = cursor.fetchone()[0]
                cursor.execute(f"INSERT INTO sync_yes (vk_id, tg_id) VALUES ({vk_id}, {tg_id})")
                conn.commit()
                await message.reply("Подтвердите привязку, проверьте личные сообщения в вк\n\n"
                                    "ВАЖНО! Необходимо убрать сообщество из ЧС, если он там есть")

                y_o_n = VkKeyboard(False, True)
                y_o_n.add_button("подтвердить ✅", VkKeyboardColor.POSITIVE, '{"yes":"sync"}')
                y_o_n.add_button("отклонить ❌", VkKeyboardColor.NEGATIVE, '{"no":"sync"}')

                vk.messages.send(peer_id=vk_id, random_id=get_random_id(),
                                 message=f"Подтвердите привязку вашего аккаунта к телеграмму",
                                 keyboard=y_o_n.get_keyboard())

            except TypeError:
                await message.reply(f"Ошибка, не нашел такого кода...")
            except IndexError:
                await message.reply(
                    f"Для привязки используйте команду:\nпривязать tg12345\n(Вместо 12345 ваш секретный код)")

    else:
        await message.reply("Ошибка!\nУ вас уже привязан вк")


@router.message(F.text.lower() == 'продолжить без фото')
async def no_photo(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user_data = cursor.fetchone()
    if user_data[6] == "text_send":
        cursor.execute(f"UPDATE users SET state = 'add_text_photo' WHERE tg_id = {tg_id}")
        conn.commit()
        await message.answer('Напишите текст, который необходимо разослать', reply_markup=keys.otmena_key)
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.message(F.text.lower() == 'продолжить без текста')
async def no_photo(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user = cursor.fetchone()
    if user[6] == "add_text_photo":
        cursor.execute(f"UPDATE users SET state = 'last_continue_photo' WHERE us_id = {user[0]}")
        conn.commit()
        cursor.execute(f"SELECT first_tg, second_tg, third_tg, id_creator FROM mailing_sending WHERE id_creator = {user[0]} and send = 0")
        info = cursor.fetchone()

        photos = []
        photo1 = InputMediaPhoto(type='photo', media=FSInputFile(f"{info[0]}"),
                                 caption=f"Вот что отправится пользователям:")
        photos.append(photo1)
        if info[1] is not None:
            photo2 = InputMediaPhoto(type='photo', media=FSInputFile(f"{info[1]}"))
            photos.append(photo2)
        if info[2] is not None:
            photo3 = InputMediaPhoto(type='photo', media=FSInputFile(f"{info[2]}"))
            photos.append(photo3)
        if info[1] is not None:
            await bot.send_media_group(chat_id=tg_id, media=photos)
            await message.answer("Все верно?", reply_markup=keys.last_photo_key)
        elif info[1] is None:
            await bot.send_photo(chat_id=tg_id, photo=FSInputFile(f"{info[0]}"),
                                 caption=f'Вот что отправится пользователям:')
            await message.answer("Все верно?", reply_markup=keys.last_photo_key)
    else:
        await message.answer('Используйте кнопки', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))


@router.message()
async def all_messages(message: Message):
    tg_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    user = cursor.fetchone()
    if user is None:
        name = message.from_user.first_name
        surname = message.from_user.last_name
        if surname is None:
            cursor.execute(f"INSERT INTO users (vk_id, tg_id, name, id_type, state) "
                           f"VALUES (0, {tg_id}, '{name}', 0, 'hello_menu')")
            conn.commit()
            await message.answer(f'Привет {name}, ты студент или абитуриент?', reply_markup=keys.hello)
        else:
            cursor.execute(f"INSERT INTO users (vk_id, tg_id, name, surname, id_type, state) "
                           f"VALUES (0, {tg_id}, '{name}', '{surname}', 0, 'hello_menu')")
            conn.commit()
            await message.answer(f'Привет {name} {surname}, ты студент или абитуриент?', reply_markup=keys.hello)
    cursor.execute(f"SELECT state FROM users WHERE tg_id = {tg_id}")
    state = cursor.fetchone()[0]
    if state == "schedule_send":
        if message.document is not None:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, f"schedule/{message.document.file_name}")
            cursor.execute(f"SELECT first_tg, second_tg, third_tg FROM mailing_sending "
                           f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and done = 0")
            send_data = cursor.fetchone()
            cursor.execute(f"SELECT us_id FROM users WHERE tg_id = {tg_id}")
            us_id = cursor.fetchone()[0]
            if send_data[0] is None:
                cursor.execute(f"UPDATE mailing_sending SET first_tg = 'schedule/{message.document.file_name}' "
                               f"WHERE id_creator = {us_id} and done = 0")
                conn.commit()
                await dwc.download_vk(f"schedule/{message.document.file_name}", us_id, 1)
                await message.answer('Успешно, желаете добавить текст?', reply_markup=keys.okey_key)
            elif (send_data[0] is not None) and (send_data[1] is None):
                cursor.execute(f"UPDATE mailing_sending SET second_tg = 'schedule/{message.document.file_name}' "
                               f"WHERE id_creator = {us_id} and done = 0")
                conn.commit()
                await dwc.download_vk(f"schedule/{message.document.file_name}", us_id, 2)
            elif (send_data[0] is not None) and (send_data[1] is not None) and (send_data[2] is not None):
                cursor.execute(f"UPDATE mailing_sending SET third_tg = 'schedule/{message.document.file_name}' "
                               f"WHERE id_creator = {us_id} and done = 0")
                conn.commit()
                await dwc.download_vk(f"schedule/{message.document.file_name}", us_id, 3)

    elif state == "add_text":
        if state == "add_text":
            if len(message.text) <= 100:
                try:
                    cursor.execute(f"UPDATE mailing_sending SET text = '{message.text}', done = 1 "
                                   f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) "
                                   f"and done = 0")
                    conn.commit()
                    wea = await ws.weather()
                    docs = []
                    cursor.execute(f"SELECT * FROM mailing_sending "
                                   f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) "
                                   f"and send = 0")
                    data = cursor.fetchone()

                    text = ""
                    if data[8] is not None:
                        text = data[8] + "\n\n" + wea + "\n(ЕСЛИ ВКЛЮЧЕНА РАССЫЛКА ПОГОДЫ)"
                    elif data[8] is None:
                        text = wea + "\n(ЕСЛИ ВКЛЮЧЕНА РАССЫЛКА ПОГОДЫ)"

                    document = FSInputFile(path=f"{data[3]}")

                    document1 = InputMediaDocument(media=FSInputFile(f"{data[3]}"), caption=text)
                    document2 = InputMediaDocument(media=FSInputFile(f"{data[5]}"))
                    document3 = InputMediaDocument(media=FSInputFile(f"{data[7]}"))

                    docs.append(document1)

                    if data[5] is not None:
                        docs.append(document2)
                    if data[7] is not None:
                        docs.append(document3)

                    if (data[5] is None) and (data[7] is None):
                        await message.answer('Вот что будет отравлено:')
                        await bot.send_document(message.chat.id, document=document, caption=text)
                        await message.answer("Подтвердите рассылку:", reply_markup=keys.last_okey_key)

                    elif (data[5] is not None) and (data[7] is not None):
                        await message.answer('Вот что будет отравлено:')
                        await bot.send_media_group(message.chat.id, media=docs)
                        await message.answer("Подтвердите рассылку:", reply_markup=keys.last_okey_key)

                    cursor.execute(f"UPDATE users SET state = 'last_continue' WHERE tg_id = {tg_id}")
                    conn.commit()

                except Exception as E:
                    print(E)
                    await message.reply('Чего-то мне плохо... Попробуй еще раз!')
            else:
                await message.reply('Слишком длинный текст, допустимо до 100 символов!')
        else:
            cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
            user_data = cursor.fetchone()
            await message.answer('Используйте кнопки!', reply_markup=keys.what_key(user_data[6], user_data[5], user_data[0]))

    if message.photo is not None and state == "text_send":
        cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
        user_data = cursor.fetchone()
        cursor.execute(f"SELECT id_send FROM mailing_sending WHERE id_creator = {user_data[0]} and done = 0")
        id_send = cursor.fetchone()[0]
        photo_id = message.photo[3].file_id
        file = await bot.get_file(photo_id)
        file_path = file.file_path
        cursor.execute(f"SELECT first_tg, second_tg, third_tg FROM mailing_sending "
                       f"WHERE id_creator = (SELECT us_id FROM users WHERE tg_id = {tg_id}) and done = 0")
        send_data = cursor.fetchone()
        cursor.execute(f"SELECT us_id FROM users WHERE tg_id = {tg_id}")
        us_id = cursor.fetchone()[0]
        if send_data[0] is None:
            cursor.execute(f"UPDATE mailing_sending SET first_tg = 'posts/{id_send}_1' "
                           f"WHERE id_creator = {us_id} and done = 0")
            await bot.download_file(file_path, f"posts/send{id_send}_1.png")
            conn.commit()
            await download_photo(id_send, 1)
            await message.answer('Успешно, теперь вы можете добавить текст', reply_markup=keys.no_text)
            cursor.execute(f"UPDATE users SET state = 'add_text_photo' WHERE tg_id = {tg_id}")
            conn.commit()
        elif (send_data[0] is not None) and (send_data[1] is None):
            cursor.execute(f"UPDATE mailing_sending SET second_tg = 'posts/{id_send}_2' "
                           f"WHERE id_creator = {us_id} and done = 0")
            await bot.download_file(file_path, f"posts/send{id_send}_2.png")
            conn.commit()
            await download_photo(id_send, 2)
        elif (send_data[0] is not None) and (send_data[1] is not None) and (send_data[2] is None):
            cursor.execute(f"UPDATE mailing_sending SET third_tg = 'posts/send{id_send}_3' "
                           f"WHERE id_creator = {us_id} and done = 0")
            await bot.download_file(file_path, f"posts/send{id_send}_3.png")
            conn.commit()
            await download_photo(id_send, 3)
    elif state == "text_send" and message.photo is None:
        await message.reply("Не нашел фото в сообщении!")
    elif state == "add_text_photo":
        text = message.text
        if len(text) < 500:
            cursor.execute(f"UPDATE mailing_sending SET text = '{text}', done = 1 WHERE id_creator = {user[0]} and done = 0")
            cursor.execute(f"UPDATE users SET state = 'last_continue_photo' WHERE us_id = {user[0]}")
            conn.commit()
            cursor.execute(f"SELECT first_tg, second_tg, third_tg, id_creator FROM mailing_sending WHERE id_creator = {user[0]} and send = 0")
            info = cursor.fetchone()
            if info[0] is not None:
                photos = []
                photo1 = InputMediaPhoto(type='photo', media=FSInputFile(f"{info[0]}"), caption=f"Вот что отправится пользователям:\n\n{text}")
                photos.append(photo1)
                if info[1] is not None:
                    photo2 = InputMediaPhoto(type='photo', media=FSInputFile(f"{info[1]}"))
                    photos.append(photo2)
                if info[2] is not None:
                    photo3 = InputMediaPhoto(type='photo', media=FSInputFile(f"{info[2]}"))
                    photos.append(photo3)
                if info[1] is not None:
                    await bot.send_media_group(chat_id=tg_id, media=photos)
                    await message.answer("Все верно?", reply_markup=keys.last_photo_key)
                elif info[1] is None:
                    await bot.send_photo(chat_id=tg_id, photo=FSInputFile(f"{info[0]}"),
                                         caption=f'Вот что отправится пользователям:\n\n{text}')
                    await message.answer("Все верно?", reply_markup=keys.last_photo_key)
            else:
                await message.answer(f'Вот что отправится пользователям:\n\n{text}')
                await message.answer("Все верно?", reply_markup=keys.last_photo_key)
        else:
            await message.reply(f"Ошибка! Допустимое количество символов - до 500.")
    else:
        cursor.execute(f"SELECT state, id_type, us_id FROM users WHERE tg_id = {tg_id}")
        data = cursor.fetchone()
        await message.answer("Используйте кнопки!", reply_markup=keys.what_key(data[0], data[1], data[2]))
'''
