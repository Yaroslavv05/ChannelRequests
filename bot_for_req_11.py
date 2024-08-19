from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sqlite3


conn = sqlite3.connect('user_database11.db')
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


bot = Bot(token='7483254621:AAGEWiE66RdV7cVFT97A8m-WbijJGMrU4HY')
storage = MemoryStorage()
CHANNEL_ID = -1002106924645
dp = Dispatcher(bot, storage=storage)


class do(StatesGroup):
    msg = State()


@dp.chat_join_request_handler()
async def on_chat_join_request(update: types.ChatJoinRequest):
    await asyncio.sleep(5)
    await update.approve()
    await bot.send_message(update.from_user.id, f"<bВітаємо, {update.from_user.full_name}! 👋 Вас додано до telegram-каналу з продажу техніки Apple!✅</b>\n\n😎 Наша команда спеціалізується на продажі останніх новинок техніки Apple та інших популярних брендів. У нашому каналі ви знайдете ексклюзивні пропозиції та професійні поради щодо вибору ідеальних гаджетів.\n\n<b>📋Детальніше ознайомитись із актуальним ассортиментом доступної до замовлення техніки та умовами придбання Ви зможете у нашому telegram-каналі - https://t.me/+OxdUt6F95NQ3N2M8</b>\n\n🍏 Наша команда вже з нетерпінням чекає на ваші замовлення та готова надати професійну допомогу у виборі техніки, яка задовольнить усі Ваші потреби.\n\n<b>📲 Для замовлення або отримання додаткової інформації, будь ласка, зверніться до нашого менеджера в Telegram: @apple_seller_opt</b>", parse_mode='HTML')
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