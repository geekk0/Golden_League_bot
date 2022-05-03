from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


trace_site_btn = InlineKeyboardButton('Сайт', callback_data='trace_site_start')
trace_stream_btn = InlineKeyboardButton("Стрим", callback_data="trace_stream_start")


admin_kb = InlineKeyboardMarkup(row_width=3).row(trace_site_btn, trace_stream_btn)


def kb_for_admin_reply(pressed_button, site_status=None, stream_status=None):
    global trace_site_btn
    global trace_stream_btn
    global admin_kb

    if pressed_button == "trace_site_start":
        trace_site_btn.callback_data = "trace_site_stop"
        trace_site_btn.text = "Сайт..." + str(site_status)

    elif pressed_button == "trace_site_stop":
        trace_site_btn.callback_data = "trace_site_start"
        trace_site_btn.text = "Сайт"

    elif pressed_button == "trace_stream_start":
        trace_stream_btn.callback_data = "trace_stream_stop"
        trace_stream_btn.text = "Стрим..." + str(stream_status)

    elif pressed_button == "trace_stream_stop":
        trace_stream_btn.callback_data = "trace_stream_start"
        trace_stream_btn.text = "Стрим"




