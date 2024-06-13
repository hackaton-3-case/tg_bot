import asyncio
import logging
from aiogram import Bot, Dispatcher
import asyncpg

import handlers_tg
from src.data.config import token_tg, url
from model import dboperations


async def main():
    #print(await dboperations.register_user('beebumbala', 'Sergey Oreshkin', '+79160019293', 'rggr@gmail.com'))
    #await dboperations.set_user_state(876545829, '{main_menu}')
    await run()
    bot = Bot(token=token_tg)
    dp = Dispatcher()
    dp.include_router(handlers_tg.router)
    print("tg bot starting..")
    await dp.start_polling(bot)


async def run():
    conn = await asyncpg.connect(url)
    #await conn.execute("DROP TABLE pets")
    #answer = await conn.execute('CREATE TABLE pets (pet_id SERIAL PRIMARY KEY, pet_type VARCHAR(10), name VARCHAR(100), town VARCHAR(100), district VARCHAR(100), sex VARCHAR(30), sterialised BOOLEAN, volunteer_id INTEGER)')
    #answer = await conn.execute('ALTER TABLE volunteers ALTER COLUMN telegram_id TYPE BIGINT')
    answer = await dboperations.get_user_data(876545829)
    print(answer)
    await conn.close()

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.WARNING)
        #logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w",
        #                    format="%(asctime)s %(levelname)s %(message)s", encoding='UTF-8')
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выключен")
