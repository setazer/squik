import os

import pyimgur
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_mng import bot, send_message
# auth_url = im.authorization_url('pin')
# webbrowser.open(auth_url)
# pin = input("What is the pin?")
# im.exchange_pin(PIN)
# album=im.get_at_url("https://imgur.com/a/cfqsiZM")
from config import config


def gen_imgur_markup(url):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text="Direct", url=url))
    return markup


@bot.message_handler(content_types=['photo'], func=lambda m: m.chat.type == "private")
def imgurize(message):
    im = pyimgur.Imgur(config['IMGUR_CLIENT_ID'], config['IMGUR_CLIENT_SECRET'])
    im.refresh_token = config['IMGUR_REFRESH_TOKEN']
    im.refresh_access_token()

    file_id = message.photo[-1].file_id
    file_obj = bot.get_file(file_id)

    file = bot.download_file(file_obj.file_path)
    with open(file_obj.file_path, 'wb') as f:
        f.write(file)

    uploaded_image = im.upload_image(path=file_obj.file_path, album=config['IMGUR_ALBUM_ID'])
    send_message(message.chat.id, "Ссылка на Imgur'е", reply_markup=gen_imgur_markup(uploaded_image.link))
    os.remove(file_obj.file_path)
    # edit_markup(message.chat.id,message.message_id,reply_markup=gen_imgur_markup(uploaded_image.link))
