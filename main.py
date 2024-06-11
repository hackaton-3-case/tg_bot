import asyncio
import logging
from aiogram import Bot, Dispatcher
import asyncpg

import dboperaations
import handlers_tg
from data.config import token_tg


async def main():
    #print(await dboperaations.register_user('Sergey Oreshkin', '+79160019293', 'rggr@gmail.com', '123456:7890'))
    await dboperaations.set_user_state(876545829, '{main_menu}')
    bot = Bot(token=token_tg)
    dp = Dispatcher()
    dp.include_router(handlers_tg.router)
    print("tg bot starting..")
    await dp.start_polling(bot)


async def run():
    conn = await asyncpg.connect('postgres://postgres:popa123@31.128.37.138:5432/nakormi_telegram_bot')
    #await conn.execute("DROP TABLE volunteers")
    #answer = await conn.execute('CREATE TABLE volunteers (volunteer_id SERIAL PRIMARY KEY , telegram_id INTEGER, fio VARCHAR(200), status INTEGER, state VARCHAR(200), phone VARCHAR(20), email VARCHAR(200), passport_data VARCHAR(50), auth_key VARCHAR(100), pets json, foods json, realised json)')
    #await conn.execute("insert into users1 (state, balance) values ('popich', 13)")
    answer = await conn.execute('ALTER TABLE volunteers ALTER COLUMN telegram_id TYPE BIGINT')
    #answer = await dboperaations.select('users1', 2)
    await conn.close()

if __name__ == '__main__':
    try:

        logging.basicConfig(level=logging.WARNING)
        #logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w",
        #                    format="%(asctime)s %(levelname)s %(message)s", encoding='UTF-8')
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выключен")
