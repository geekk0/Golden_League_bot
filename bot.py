import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, admin_list, admin_listeners
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


async def admin_reply(callback_query=None, site_status=None, stream_status=None):

    if site_status:
        status = {"resource": "site", "status": site_status}
    elif stream_status:
        status = {"resource": "stream", "status": stream_status}
    else:
        status = None

    if kb_for_admin_reply(pressed_button=callback_query.data, status=status):

        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                                message_id=callback_query.message.message_id, reply_markup=admin_kb)


async def trace_site_start(active_listeners):
    global site_error

    await admin_reply(callback_query, site_status=None)

    try:
        requests.get(url="http://188.225.38.178:4000")
        site_status = "Up"

        if site_error:
            await send_service_messages(admin_listeners, "Сайт поднялся")
            site_error = False
    except Exception as e:
        site_status = "Down"
        await admin_reply(callback_query, site_status)
        if not site_error:
            await send_service_messages(admin_listeners, "Сайт не отвечает")
            site_error = True
            logging.error(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Сайт не отвечает" + " " + str(e)))
    await asyncio.sleep(5)

trace_site_start(admin_listeners)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    if message.chat.id in admin_list:

        admin_listeners[message.chat.id] = message.message_id
    
        await message.answer("Интерфейс администратора: ", reply_markup=admin_kb)


@dp.callback_query_handler(lambda c: c.data == 'trace_site_start')
async def active_listener(callback_query: types.CallbackQuery):
    await admin_listeners.append(callback_query.message.chat.id)
    await admin_reply(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'trace_site_stop')
async def remove_listener(callback_query: types.CallbackQuery):
    await admin_listeners.remove(callback_query.message.chat.id)
    await admin_reply(callback_query)


@dp.callback_query_handler(lambda c: c.data == 'trace_stream_start')
async def trace_stream_start(callback_query: types.CallbackQuery):
    global stop_trace_stream
    global stream_error
    stop_trace_stream = False

    while not stop_trace_stream:
        try:
            requests.get(url="http://188.225.38.178:4000")
            stream_status = "Up"
            if stream_error:
                await send_service_messages(admin_listeners, "Стрим поднялся")
                stream_error = False

        except Exception as e:
            stream_status = "Down"
            if not stream_error:
                await send_service_messages(admin_listeners, "Стрим не отвечает")

                stream_error = True
                logging.error(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Стрим не отвечает" + " " + str(e)))

        # await admin_reply(callback_query, "Отслеживание стрима запущено", stream_status)
        await asyncio.sleep(3)


@dp.callback_query_handler(lambda c: c.data == 'trace_stream_stop')
async def trace_stream_stop(callback_query: types.CallbackQuery):
    global stop_trace_stream
    stop_trace_stream = True
    # await admin_reply(callback_query, "Отслеживание стрима остановлено")


if __name__ == "__main__":
    executor.start_polling(dp)
