from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sqlite3


conn = sqlite3.connect('user_database5 .db')
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


bot = Bot(token='6140136097:AAEAOAGlmMSowVdtAgtCUcaWF6lfpaYl9dA')
storage = MemoryStorage()
CHANNEL_ID = -1002035916230
dp = Dispatcher(bot, storage=storage)


class do(StatesGroup):
    msg = State()


@dp.chat_join_request_handler()
async def on_chat_join_request(update: types.ChatJoinRequest):
    await asyncio.sleep(5)
    await update.approve()
    await bot.send_message(update.from_user.id, f"<b>Вітаю, {update.from_user.full_name}!🌸 Твоя заявка на вступ у Telegram канал схвалена! ✨</b>\n\n😊 Мене звуть Кравченко Анна, і я баєр продукції Dyson та іншої бьюті-техніки з Європи🇪🇺\nУ моєму телеграм каналі кожна сучасна жінка знайде щось особливе для себе!\n\n<b>🛒 Я роблю ваше життя більш комфортним та стильним, викупаючи найкращу техніку Dyson з офіційних магазинів із чеками та гарантією за найвигіднішими цінами, а також з надзвичайно швидкою доставкою📦</b>\n\n🎁 Щоб дізнатися більше та замовити бажану техніку, просто напишіть мені «+» в особисті повідомлення. Я завжди рада допомогти вам обрати і придбати ідеальні речі для вашої краси!\n\n<b>📲 Для зручного здійснення замовлення звертайтесь у мій Telegram: @dyson_bayer_kravchenko</b>", parse_mode='HTML')
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