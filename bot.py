import logging
import requests
import time

from aiogram import Bot, Dispatcher, executor, types
from ntoken import TOKEN
from datetime import datetime

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(filename='log_file.log', level=logging.INFO)
stop_trace_site = False
stop_trace_stream = False


@dp.message_handler(commands="trace_site")
async def cmd_test1(message: types.Message):
    global stop_trace_site
    stop_trace_site = False

    while not stop_trace_site:
        try:
            status = requests.get(url="http://188.225.38.178:4000").status_code
        except Exception as e:
            await message.answer("Сайт не отвечает")
            logging.error(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Сайт не отвечает" + " " + str(e)))
            time.sleep(60)

        time.sleep(2)


async def stop_site(message: types.Message):
    global stop_trace_site
    stop_trace_site = True
    await message.answer("Отслеживание сайта остановлено")


@dp.message_handler(commands="trace_stream")
async def trace_stream(message: types.Message):
    global stop_trace_stream
    stop_trace_stream = False

    while not stop_trace_stream:
        status = requests.get(url="https://golden-league.pro/hls_stream/stream.m3u8").status_code

        if status != 200:
            await message.answer("Стрим не отвечает")
        else:
            await message.answer("Стрим в порядке")
        time.sleep(2)


async def stop_stream(message: types.Message):
    global stop_trace_stream
    stop_trace_stream = True
    await message.answer("Отслеживание стрима остановлено")


dp.register_message_handler(stop_site, commands="stop_trace_site")
dp.register_message_handler(stop_stream, commands="stop_trace_stream")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)