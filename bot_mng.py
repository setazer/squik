import datetime as dt
import os
import time
from functools import wraps

import requests
import telebot

from config import config
from util import log_error

# telebot.apihelper.proxy = config['REQUESTS_PROXY']
bot = telebot.TeleBot(config['TELEGRAM_TOKEN'], skip_pending=True)
bot.users = {}
bot.shutting_down = False
bot.start_time = dt.datetime.fromtimestamp(time.time())
bot.error_msg = None
# wrappers
def action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        err_wait = [1, 5, 15, 30, 60, 300]
        retval = None
        for i in range(20):
            try:
                retval = func(*args, **kwargs)
            except requests.exceptions.ConnectionError as exc:
                time.sleep(err_wait[min(i, 5)])
                log_error(exc, args, kwargs)
            except (telebot.apihelper.ApiException, FileNotFoundError) as exc:
                log_error(exc, args, kwargs)
                break
            except Exception as exc:
                log_error(exc, args, kwargs)
                time.sleep(err_wait[min(i, 3)])
            else:
                break
        return retval

    return wrapper


def access(access_number=0):
    def decorator(func):
        @wraps(func)
        def wrapper(message, *args):
            user_access = bot.users[message.from_user.id]['access'] if message.from_user.id in bot.users else 0
            if user_access >= access_number:
                func(message, *args)
            elif user_access > 0:
                if isinstance(message, telebot.types.CallbackQuery):
                    answer_callback(message.id, "Not allowed!")
                else:
                    send_message(message.from_user.id, "Not allowed!")

        return wrapper

    return decorator


bot.action = action
bot.access = access

# wrappers end

# bot main actions
@bot.action
def send_message(chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                 parse_mode=None, disable_notification=None):
    return bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview=disable_web_page_preview,
                            reply_to_message_id=reply_to_message_id, reply_markup=reply_markup,
                            parse_mode=parse_mode, disable_notification=disable_notification)

@bot.action
def edit_message(text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                 disable_web_page_preview=None, reply_markup=None):
    return bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id,
                                 inline_message_id=inline_message_id,
                                 parse_mode=parse_mode,
                                 disable_web_page_preview=disable_web_page_preview, reply_markup=reply_markup)


@bot.action
def edit_markup(chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    return bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                         inline_message_id=inline_message_id, reply_markup=reply_markup)


@bot.action
def delete_message(chat_id, message_id):
    return bot.delete_message(chat_id=chat_id, message_id=message_id)


@bot.action
def forward_message(chat_id, from_chat_id, message_id, disable_notification=None):
    return bot.forward_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id,
                               disable_notification=disable_notification)


@bot.action
def send_chat_action(chat_id, action):
    return bot.send_chat_action(chat_id=chat_id, action=action)

@bot.action
def send_photo(chat_id, photo_filename, caption=None, reply_to_message_id=None, reply_markup=None,
               disable_notification=None):
    if os.path.exists(photo_filename):
        with open(photo_filename, 'rb') as photo:
            return bot.send_photo(chat_id=chat_id, photo=photo, caption=caption,
                                  reply_to_message_id=reply_to_message_id,
                                  reply_markup=reply_markup,
                                  disable_notification=disable_notification)
    else:
        return bot.send_photo(chat_id=chat_id, photo=photo_filename, caption=caption,
                              reply_to_message_id=reply_to_message_id,
                              reply_markup=reply_markup,
                              disable_notification=disable_notification)


@bot.action
def answer_callback(callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
    return bot.answer_callback_query(callback_query_id=callback_query_id, text=text, show_alert=show_alert, url=url,
                                     cache_time=cache_time)


@bot.action
def send_document(chat_id, data_filename, reply_to_message_id=None, caption=None, reply_markup=None,
                  parse_mode=None, disable_notification=None, timeout=None):
    if os.path.exists(data_filename):
        with open(data_filename, 'rb') as data:
            return bot.send_document(chat_id=chat_id, data=data, reply_to_message_id=reply_to_message_id,
                                     caption=caption, reply_markup=reply_markup,
                                     parse_mode=parse_mode, disable_notification=disable_notification, timeout=timeout)
    else:
        return bot.send_document(chat_id=chat_id, data=data_filename, reply_to_message_id=reply_to_message_id,
                                 caption=caption, reply_markup=reply_markup,
                                 parse_mode=parse_mode, disable_notification=disable_notification, timeout=timeout)
# bot main actions end

def msg_to_owner(text):
    return send_message(config['OWNER_ID'], str(text))
