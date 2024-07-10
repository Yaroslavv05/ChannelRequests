from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sqlite3


conn = sqlite3.connect('user_database10.db')
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


bot = Bot(token='6725118263:AAEDVo3BfBjsRdfty2vU8ZOMsQGe8SYMwe0')
storage = MemoryStorage()
CHANNEL_ID = -1002182631669
dp = Dispatcher(bot, storage=storage)


class do(StatesGroup):
    msg = State()


@dp.chat_join_request_handler()
async def on_chat_join_request(update: types.ChatJoinRequest):
    await asyncio.sleep(5)
    await update.approve()
    await bot.send_message(update.from_user.id, f"<b>Witaj, {update.from_user.full_name}! 🌟 Z powodzeniem dołączyłeś do naszej elitarnej społeczności arbitrażu kryptowalutowego na Telegramie! ✅</b>\n\n🚀 Ja, Mirosław Sokołowski, jestem założycielem i szefem zespołu arbitrażowego, a także właścicielem tego wyjątkowego kanału Telegram, na którym dzielimy się sekretami skutecznego arbitrażu kryptowalutowego. Tutaj znajdziesz najnowsze odkrycia, dogłębne analizy i sprawdzone strategie optymalizacji zysków.\n\n<b>🔍 Arbitraż to nie tylko nasza pasja, ale także niezawodna droga do niezależności finansowej. Zapraszamy do dołączenia do nas na warunkach współpracy, które zapewnią obopólne korzyści - nasze wynagrodzenie jest oparte na Twoim zysku, ale dopiero wtedy, gdy zaczniesz osiągać realne dochody! 💰</b>\n\n📩 Jeśli jesteś gotowy, aby zanurzyć się głębiej w świat arbitrażu i chcesz dowiedzieć się więcej o naszych metodach i możliwościach współpracy, wyślij mi "+" w wiadomościach prywatnych.\n\n<b>🔗 Dla wygodnej komunikacji zostawiam moje dane kontaktowe na Telegramie: @trader_miroslaw</b>", parse_mode='HTML')
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