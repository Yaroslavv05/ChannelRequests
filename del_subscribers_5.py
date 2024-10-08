import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

TOKEN = "6799712562:AAEv2dTm3nkMJuwFaO_JoCP12U1t1Qu6pno"

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

CHAT_ID = '-1001581435062'

dp = Dispatcher()


@dp.channel_post()
@dp.message(Command('remove'))
async def echo_handler(message: types.Message) -> None:
    try:
        await bot.ban_chat_member(chat_id=CHAT_ID, user_id=message.text.split()[1])
        await bot.send_message(message.from_user.id, 'Пользователь был забанен')
    except Exception as e:
        print(e)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())