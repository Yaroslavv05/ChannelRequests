from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sqlite3


conn = sqlite3.connect('user_database12.db')
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


bot = Bot(token='6421326160:AAFDO7g4ns3jtJMWvWn_UbqpplMXD0GwGBY')
storage = MemoryStorage()
CHANNEL_ID = -1002159286207
dp = Dispatcher(bot, storage=storage)


class do(StatesGroup):
    msg = State()


@dp.chat_join_request_handler()
async def on_chat_join_request(update: types.ChatJoinRequest):
    await asyncio.sleep(5)
    await update.approve()
    await bot.send_message(
    update.from_user.id,
    f"<b>Вітаємо, {update.from_user.full_name}! ✌️ Ви щойно стали частиною нашої Telegram-спільноти з арбітражу криптовалюти! ✅</b>\n\n😎 Мене звати Дмитро Гордієнко, і я є засновником та керівником арбітражної команди, а також автором цього унікального каналу. Тут ми розкриваємо секрети ефективного криптовалютного арбітражу. На нашому каналі ви отримаєте доступ до найсвіжіших інсайдів, глибоких аналітик та перевірених стратегій для максимізації ваших прибутків.\n\n<b>📈 Арбітраж для нас — це більше, ніж просто захоплення; це надійний шлях до фінансової свободи. Запрошуємо вас приєднатися до нас на умовах співпраці, які приносять користь обом сторонам – ми заробляємо тільки тоді, коли ви починаєте отримувати реальний дохід! 💸</b>\n\n📩 Якщо ви готові заглибитися в світ арбітражу та бажаєте дізнатися більше про наші методи та можливості співпраці, надішліть мені '+' у приватні повідомлення.\n\n<b>📲 Для зручності залишаю свої контактні дані в Telegram: @gordienko_crypto</b>",
    parse_mode='HTML')   
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