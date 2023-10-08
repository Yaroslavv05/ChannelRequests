from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sqlite3


conn = sqlite3.connect('user_database4.db')
cursor = conn.cursor()

# Создаем таблицу для хранения userid
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        userid TEXT NOT NULL
    )
''')


def insert_userid(userid):
    cursor.execute('INSERT INTO users (userid) VALUES (?)', (userid,))
    conn.commit()


def get_userids():
    cursor.execute('SELECT userid FROM users')
    return cursor.fetchall()


bot = Bot(token='6354113727:AAG13g07jf1Ecj3wT6RtbX3QG7vZIDLzXIg')
storage = MemoryStorage()
CHANNEL_ID = -1001943373065
dp = Dispatcher(bot, storage=storage)


class do(StatesGroup):
    msg = State()


@dp.chat_join_request_handler()
async def on_chat_join_request(update: types.ChatJoinRequest):
    await asyncio.sleep(5)
    await update.approve()
    await bot.send_message(update.from_user.id, f"<b>Вітаю, {update.from_user.full_name}! 🤝 Вас прийнято у нашу телеграм групу✅</b>\n\n👨😎 Мене звати Олексій і я власник команди та особистого блогу по заробітку на криптовалюті і арбітражі. У власному блозі я даю детальні звʼязки та приватні інструкції по заробітку.\n\n<b>💰 Для нас це головне джерело заробітку, тому ми співпрацюємо за % від Вашого чистого прибутку, лише після отримання Вами доходу!</b>\n\n📩 Для отримання інформації та початку співпраці напишіть мені '+' в особисті повідомлення\n\n<b>📲Мої контактні дані у телеграм для здійснення звʼязку:\n@kravchenko_trade</b>", parse_mode='HTML')
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

scheduler.start()


if __name__ == "__main__":
    print("ONLINE")
    executor.start_polling(dp, skip_updates=True)