import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, executor
from config import TOKEN, admin_list
from datetime import datetime

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(filename='log_file.log', level=logging.INFO)
stop_trace_site = False
stop_trace_stream = False
site_error = False
stream_error = False


@dp.message_handler(commands="trace_site")
async def trace_site(message):
    global stop_trace_site
    global site_error
    stop_trace_site = False

    await send_service_messages(admin_list, "Отслеживание сайта запущено", message)

    while not stop_trace_site:
        try:
            requests.get(url="https://golden-league.pro")
            if site_error:
                await send_service_messages(admin_list, "Сайт поднялся", message)
                site_error = False
        except Exception as e:
            if not site_error:
                await send_service_messages(admin_list, "Сайт не отвечает", message)
                site_error = True
                logging.error(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Сайт не отвечает" + " " + str(e)))

        await asyncio.sleep(3)


async def stop_site(message):
    global stop_trace_site
    stop_trace_site = True
    await send_service_messages(admin_list, "Отслеживание сайта остановлено", message)


@dp.message_handler(commands="trace_stream")
async def trace_stream(message):
    global stop_trace_stream
    global stream_error
    stop_trace_stream = False

    await send_service_messages(admin_list, "Отслеживание стрима запущено", message)

    while not stop_trace_stream:

        try:
            requests.get(url="https://golden-league.pro/hls_stream/stream.m3u8")
            if stream_error:
                await send_service_messages(admin_list, "Стрим поднялся", message)
                stream_error = False
        except Exception as e:
            if not stream_error:
                await send_service_messages(admin_list, "Стрим не отвечает", message)
                stream_error = True
                logging.error(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Стрим не отвечает" + " " + str(e)))

        await asyncio.sleep(3)


async def stop_stream(message):
    global stop_trace_stream
    stop_trace_stream = True
    await send_service_messages(admin_list, "Отслеживание стрима остановлено", message)


async def send_service_messages(recipients, text, message):
    for admin_chat_id in recipients:
        await bot.send_message(int(admin_chat_id), text)
        logging.debug(message)


dp.register_message_handler(stop_site, commands="stop_trace_site")
dp.register_message_handler(stop_stream, commands="stop_trace_stream")


if __name__ == "__main__":
    executor.start_polling(dp)
