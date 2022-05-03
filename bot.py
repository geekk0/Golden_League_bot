import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, admin_list
from datetime import datetime

from keyboards import admin_kb, kb_for_admin_reply

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(filename='log_file.log', level=logging.INFO)
stop_trace_site = False
stop_trace_stream = False
site_error = False
stream_error = False


async def send_service_messages(recipients, text):
    for admin_chat_id in recipients:
        await bot.send_message(int(admin_chat_id), text)


async def admin_reply(callback_query, text):
    kb_for_admin_reply(callback_query.data)
    await bot.edit_message_text(text=text, chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id, reply_markup=admin_kb)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    
    await message.answer("Интерфейс администратора: ", reply_markup=admin_kb)


@dp.callback_query_handler(lambda c: c.data == 'trace_site_start')
async def trace_site_start(callback_query: types.CallbackQuery):
    global stop_trace_site
    global site_error
    stop_trace_site = False

    await admin_reply(callback_query, "Отслеживание сайта запущено")

    while not stop_trace_site:
        try:
            requests.get(url="http://188.225.38.178:4000")
            kb_for_admin_reply("trace_site_start", site_status="Up")

            if site_error:
                await send_service_messages(admin_list, "Сайт поднялся")
                site_error = False
        except Exception as e:
            kb_for_admin_reply("trace_site_start", site_status="Down")
            if not site_error:
                await send_service_messages(admin_list, "Сайт не отвечает")
                site_error = True
                logging.error(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Сайт не отвечает" + " " + str(e)))

        await asyncio.sleep(3)


@dp.callback_query_handler(lambda c: c.data == 'trace_site_stop')
async def trace_site_stop(callback_query: types.CallbackQuery):
    global stop_trace_site
    stop_trace_site = True
    await admin_reply(callback_query, "Отслеживание сайта остановлено")


@dp.callback_query_handler(lambda c: c.data == 'trace_stream_start')
async def trace_stream_start(callback_query: types.CallbackQuery):
    global stop_trace_stream
    global stream_error
    stop_trace_stream = False

    await admin_reply(callback_query, "Отслеживание стрима запущено")

    while not stop_trace_stream:
        try:
            requests.get(url="http://188.225.38.178:4000")
            kb_for_admin_reply("trace_stream_start", stream_status="Up")

            if stream_error:
                await send_service_messages(admin_list, "Стрим поднялся")
                stream_error = False

        except Exception as e:
            kb_for_admin_reply("trace_stream_start", stream_status="Down")
            if not stream_error:
                await send_service_messages(admin_list, "Стрим не отвечает")

                stream_error = True
                logging.error(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Стрим не отвечает" + " " + str(e)))

        await asyncio.sleep(3)


@dp.callback_query_handler(lambda c: c.data == 'trace_stream_stop')
async def trace_stream_stop(callback_query: types.CallbackQuery):
    global stop_trace_stream
    stop_trace_stream = True
    await admin_reply(callback_query, "Отслеживание стрима остановлено")


if __name__ == "__main__":
    executor.start_polling(dp)
