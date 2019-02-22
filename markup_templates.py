# -*- coding: utf-8 -*-

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_user_limit_markup(users):
    user_limit_markup = InlineKeyboardMarkup()
    user_limit_markup.row_width = 2
    buttons = []
    for user, data in users.items():
        buttons.append(
            InlineKeyboardButton(f"{data['username'] or user}: {data['limit']}", callback_data=f"limit{user}"))
    user_limit_markup.add(*buttons)
    return user_limit_markup


def gen_user_markup(user):
    user_markup = InlineKeyboardMarkup()
    user_markup.row_width = 2
    user_markup.add(InlineKeyboardButton("Да", callback_data=f"user_allow{user}"),
                    InlineKeyboardButton("Нет", callback_data=f"user_deny{user}"))
    user_markup.row(InlineKeyboardButton("Забанить", callback_data=f"user_block{user}"))
    return user_markup


def gen_status_markup(*args):
    status_markup = InlineKeyboardMarkup()
    for arg in args:
        status_markup.row(
            InlineKeyboardButton(text=arg, callback_data='progress'))
    return status_markup