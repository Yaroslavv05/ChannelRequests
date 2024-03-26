from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sqlite3


conn = sqlite3.connect('user_database9.db')
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


bot = Bot(token='6835959621:AAFDugBHJ3zxGNFKvT8XMj3ZjprMD4mihVA')
storage = MemoryStorage()
CHANNEL_ID = -1001581435062
dp = Dispatcher(bot, storage=storage)


class do(StatesGroup):
    msg = State()


@dp.chat_join_request_handler()
async def on_chat_join_request(update: types.ChatJoinRequest):
    await asyncio.sleep(5)
    await update.approve()
    await bot.send_message(update.from_user.id, f"<b>Ласкаво просимо, {update.from_user.full_name}!🌟 Ви успішно долучені до нашої елітної спільноти з арбітражу криптовалюти у Telegram! ✅</b>\n\n🚀 Я, Олександр Міранчук, засновник та голова арбітражної команди, а також власник цього унікального телеграм-каналу, де ми ділимося секретами ефективного арбітражу криптовалют. Тут ви знайдете останні знахідки, глибокі аналізи та перевірені стратегії для оптимізації вашого прибутку.\n\n<b>🔍 Арбітраж — це не лише наша пристрасть, але й надійний шлях до фінансової незалежності. Запрошуємо вас долучитися до нас на умовах співпраці, які забезпечать взаємну вигоду – наша винагорода базується на вашому прибутку, але тільки після того, як ви почнете отримувати реальний дохід! 💰</b>\n\n📩 Якщо ви готові зануритися в світ арбітражу глибше і хочете дізнатися більше про наші методи та можливості співпраці, відправте мені '+' у приватні повідомлення.\n\n<b>🔗 Для зручного спілкування, залишаю для вас мої контактні дані у Telegram: @trader_miranchuk</b>", parse_mode='HTML')
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