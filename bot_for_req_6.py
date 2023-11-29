from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sqlite3


conn = sqlite3.connect('user_database6 .db')
cursor = conn.cursor()

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


bot = Bot(token='6518229742:AAEtx0XuRtOlz7sT0KmCYYuxttl5nDjP8PA')
storage = MemoryStorage()
CHANNEL_ID = -1002146768767
dp = Dispatcher(bot, storage=storage)


class do(StatesGroup):
    msg = State()


@dp.chat_join_request_handler()
async def on_chat_join_request(update: types.ChatJoinRequest):
    await asyncio.sleep(5)
    await update.approve()
    await bot.send_message(update.from_user.id, f"<b>Ласкаво просимо, {update.from_user.full_name}!🤝 Вітаю у нашій телеграм-спільноті✅</b>\n\n😊😎 Мене звуть Роман, і я - засновник арбітражної команди та власник особистого блогу, присвяченого заробітку на криптовалюті та арбітражу. В своєму каналі я ділюся докладними вказівками та унікальними порадами з питань заробітку у криптовалюті.\n\n<b>💰 Для нас це важливе джерело прибутку, тому пропонуємо співпрацю на вигідних умовах - ми беремо % від вашого чистого доходу, але тільки після того, як ви отримаєте свій прибуток!</b>\n\n📩 Щоб отримати додаткову інформацію та розпочати співпрацю, просто напишіть мені '+' в особисті повідомлення.\n\n<b>📲 Для зручного зв'язку, залишаю свої контактні дані у Telegram: @tkachenko_arbitrage</b>", parse_mode='HTML')
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