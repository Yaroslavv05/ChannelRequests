from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sqlite3


conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

# Создаем таблицу для хранения userid
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        userid TEXT NOT NULL
    )
''')


# Пример вставки данных в таблицу
def insert_userid(userid):
    cursor.execute('INSERT INTO users (userid) VALUES (?)', (userid,))
    conn.commit()


def get_userids():
    cursor.execute('SELECT userid FROM users')
    return cursor.fetchall()


bot = Bot(token='6311307131:AAG-c5YV8TCDccMWsNdwB-xkSzV0X0sFUNc')
storage = MemoryStorage()
CHANNEL_ID = -1001918816977
dp = Dispatcher(bot, storage=storage)


class do(StatesGroup):
    msg = State()


@dp.chat_join_request_handler()
async def on_chat_join_request(update: types.ChatJoinRequest):
    await asyncio.sleep(5)
    await update.approve()
    await bot.send_message(update.from_user.id, f"<b>Привіт {update.from_user.full_name}! 🤝 Твою заявку в групу схвалено✅</b>\n\n👨‍💻 Моє ім'я Микола, я веду блог із заробітку на криптовалюті. У своєму каналі я даю приватні інструкції та зв'язки.\n\n<b>💸 Для мене це важливий Бізнес, тому ми працюємо за % від чистого прибутку, \nале тільки після того, як ви заробили!</b>\n\n🏆 Пиши мені '+' в ЛС для отримання детальної інформації\n\n<b>Мій телеграмм канал для зв'язку @crypto_fadeev_ua</b>", parse_mode='HTML')
    insert_userid(update.from_user.id)


@dp.message_handler(commands=['black_live_matter'])
async def welcome(message: types.Message):
    await do.msg.set()
    await bot.send_message(message.from_user.id, f'Введи сообщение, которое надо будет разослать:')


async def send_scheduled_message(user_id, message):
    await bot.send_message(user_id, message)


@dp.message_handler(state=do.msg)
async def input_symbol(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text
    for row in get_userids():
        await send_scheduled_message(user_id=row[0], message=data['msg'])
    await message.answer("Рассылка выполнена!")
    await state.finish()


scheduler = AsyncIOScheduler()

# Запуск планировщика
scheduler.start()


if __name__ == "__main__":
    print("ONLINE")
    executor.start_polling(dp, skip_updates=True)