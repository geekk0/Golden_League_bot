from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


trace_site_btn = InlineKeyboardButton('Сайт', callback_data='trace_site_start')
trace_stream_btn = InlineKeyboardButton("Стрим", callback_data="trace_stream_start")


admin_kb = InlineKeyboardMarkup(row_width=3).row(trace_site_btn, trace_stream_btn)


def kb_for_admin_reply(pressed_button, status=None):
    global trace_site_btn
    global trace_stream_btn
    global admin_kb

    print(pressed_button)
    print(status)

    if pressed_button == "trace_site_start":
        if status:
            if status["resource"] == "site" and trace_site_btn.text != "Сайт..." + status["status"]:
                trace_site_btn.text = "Сайт..." + status["status"]
                return True
            else:
                return False

        else:
            trace_site_btn.callback_data = "trace_site_stop"
            return True

    elif pressed_button == "trace_site_stop":
        trace_site_btn.callback_data = "trace_site_start"
        trace_site_btn.text = "Сайт"

        return True


def start_stop_kb(button):

    global trace_site_btn
    global admin_kb

    print(button)
    if button == "trace_site_start":
        trace_site_btn.callback_data = "trace_site_stop"
        return True
    if button == "trace_site_stop":
        trace_site_btn.callback_data = "trace_site_start"
        trace_site_btn.text = "Сайт"


def btn_status_update(status):
    global trace_site_btn

    if trace_site_btn.text != "Сайт..." + status:
        trace_site_btn.text = "Сайт..." + status
        return True
    else:
        return False






