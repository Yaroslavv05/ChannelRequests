from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sqlite3


conn = sqlite3.connect('user_database8 .db')
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


bot = Bot(token='6701752436:AAGmfQ5DBXh1z4hNMfibvFyRZXUyO1m-_WM')
storage = MemoryStorage()
CHANNEL_ID = -1002132375545
dp = Dispatcher(bot, storage=storage)


class do(StatesGroup):
    msg = State()


@dp.chat_join_request_handler()
async def on_chat_join_request(update: types.ChatJoinRequest):
    await asyncio.sleep(5)
    await update.approve()
    await bot.send_message(update.from_user.id, f"<b>Запрошуємо, {update.from_user.full_name}!🤝 Вас додано до нашої трейдинг-спільноти у телеграм! ✅</b>\n\n🤓 Моє ім’я Дмитро Соколов, я засновник і керівник трейдингової команди та власник телеграм-каналу, присвяченого заробітку на торгівлі криптовалютними активами. В даній спільності ми щодня публікуємо перевірені та детальні стратегії і прибуткові крипто угоди.\n\n<b>📊 Ми вважаємо трейдинг не просто хобі, а реальним джерелом доходу. Тому запрошуємо до співпраці на умовах, що будуть вигідні для обох сторін - ми отримуємо комісію з вашого прибутку, але лише після того, як ви почнете заробляти!💸</b>\n\n📩 Якщо вас цікавить додаткова інформація та ви готові до співпраці, просто відправте мені символ '+' в особисті повідомлення.\n\n<b>📲 Для зручного зв'язку, надаю свої контактні дані у Telegram: @dm_sokolov_trade</b>", parse_mode='HTML')
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