from aiogram import Bot, Dispatcher, types
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from aiogram.utils import executor
from aiogram.types.web_app_info import WebAppInfo

API_TOKEN = '7241785314:AAGQ20IziGju6fQMKWVD0V2aqrxIlirl6_g'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Отправляем веб-страницу в ответ на команду /start
    await message.answer("Hello! Press the button below to open the web app.", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("Open PointSwap", web_app=WebAppInfo(url="https://light.any-trade.org/for-telegram.php"))
    ))

@dp.message_handler(content_types=types.ContentTypes.WEB_APP_DATA)
async def web_app_data_handler(web_app_data: types.WebAppData):
    # Обработка данных, полученных от веб-приложения
    data = web_app_data.data  # Ваша логика обработки данных

    # Например, отправка данных обратно пользователю
    await web_app_data.message.answer(f"Data received: {data}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
