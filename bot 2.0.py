import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, admin_list
from datetime import datetime
from keyboards import admin_kb, start_stop_kb, btn_status_update

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(filename='log_file.log', level=logging.INFO)
site_error = False
current_admin_list = admin_list


async def send_service_messages(resource, text):
    global current_admin_list

    for admin_chat_id in current_admin_list.keys():
        print("/send_service_messages" + str(current_admin_list))
        if resource in current_admin_list[admin_chat_id]:
            await bot.delete_message(admin_chat_id, current_admin_list[admin_chat_id][0])
            await save_admins()
            await bot.send_message(int(admin_chat_id), text, reply_markup=admin_kb)
            current_admin_list[admin_chat_id][0] += 1


async def edit_status_button(status):
    global current_admin_list

    for admin_chat_id in current_admin_list.keys():
        print("/edit_status_btn" + str(current_admin_list))

        if current_admin_list[admin_chat_id][1] == "site" and btn_status_update(status):

            try:
                await bot.edit_message_reply_markup(admin_chat_id, current_admin_list[admin_chat_id][0],
                                                    reply_markup=admin_kb)
            except:
                await bot.send_message(admin_chat_id, "Интерфейс администратора: ", reply_markup=admin_kb)


async def save_admins():
    global current_admin_list

    f = open("config.py", "w")
    block = "TOKEN = " + "'" + str(TOKEN) + "'" + "\n"
    block += "admin_list = " + str(admin_list) + "\n"
    f.write(block)
    f.close()


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    global current_admin_list

    if message.chat.id in current_admin_list.keys():
        current_admin_list[message.chat.id][0] = message.message_id
        print("/admin" + str(current_admin_list))
        await message.answer("Интерфейс администратора: ", reply_markup=admin_kb)


@dp.message_handler(commands=['show_listeners'])
async def admin(message: types.Message):
    await message.answer(str(current_admin_list))


@dp.message_handler(commands=["my_chat_id"])
async def my_chat(message: types.Message):
    await message.answer("Чат id: " + str(message.chat.id))


@dp.message_handler(commands=['global_trace_site'])
async def global_trace_site(message: types.Message):
    global site_error

    while True:
        try:
            requests.get(url="http://188.225.38.178:4000")
            site_status = "Up"
            await edit_status_button(site_status)
            if site_error:
                site_error = False
                await send_service_messages("site", "Сайт поднялся")
        except Exception as e:
            site_status = "Down"
            await edit_status_button(site_status)
            if not site_error:
                await send_service_messages("site", "Сайт не отвечает")
                site_error = True
                logging.error(str(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Сайт не отвечает" + " " + str(e)))
        await asyncio.sleep(3)


@dp.callback_query_handler(lambda c: 'trace_site' in c.data)
async def activate_listener(callback_query: types.CallbackQuery):
    global current_admin_list

    if "start" in callback_query.data:
        start_stop_kb("trace_site_start")
        current_admin_list[callback_query.message.chat.id][0] = callback_query.message.message_id
        current_admin_list[callback_query.message.chat.id][1] = "site"
        await save_admins()

    else:
        current_admin_list[callback_query.message.chat.id][0] = callback_query.message.message_id
        current_admin_list[callback_query.message.chat.id][1] = "None"
        await save_admins()

        start_stop_kb("trace_site_stop")

    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=admin_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
