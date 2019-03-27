# -*- coding: utf-8 -*-
import argparse
import logging

import flask
import telebot

import importdir
import util
from bot_mng import bot, edit_message, msg_to_owner, send_chat_action
from config import config
from db_mng import User, session_scope


def main():
    def load_users():
        o_logger.debug("Loading users")
        with session_scope() as session:
            bot.users = {user: {"access": access, "limit": limit} for user, access, limit in
                         session.query(User.user_id, User.access, User.limit).all()}
        if not bot.users:
            bot.users = {config['OWNER_ID']: {"access": 100}}
        o_logger.debug(f'Loaded users: {", ".join(str(user) for user in bot.users.keys())}')

    logging.Logger.propagate = False
    o_logger = logging.getLogger('OhaioPosterLogger')
    o_logger.propagate = False
    o_logger.setLevel(logging.DEBUG if args.debugging else logging.INFO)
    if args.debugging:
        telebot.logger.setLevel(logging.DEBUG)
    o_fh = logging.FileHandler(config['LOG_FILE'])
    o_fh.setLevel(logging.DEBUG)
    o_fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [Listener] %(message)s"))
    o_ch = logging.StreamHandler()
    o_ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [Listener] %(message)s"))
    o_ch.setLevel(logging.ERROR)
    o_logger.addHandler(o_fh)
    o_logger.addHandler(o_ch)

    o_logger.debug("Initializing bot")
    load_users()

    app = flask.Flask(__name__)

    @app.route(f"/{config['TELEGRAM_TOKEN']}", methods=['POST'])
    def webhook():
        if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.stream.read().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return "!", 200
        else:
            flask.abort(403)

    # Empty webserver index, return nothing, just http 200
    @app.route('/', methods=['GET', 'HEAD'])
    def index():
        bot.remove_webhook()
        bot.set_webhook(url=config['WEBHOOK_URL'] + config['TELEGRAM_TOKEN'])
        return "!", 200

    importdir.do("handlers", globals())
    #
    # @bot.callback_query_handler(func=lambda call: True)
    # @bot.access(1)
    # def callback_query(call):
    #     pass

    for user in (user for user, user_data in bot.users.items() if user_data['access'] > 1):
        send_chat_action(user, 'typing')
    for i in range(1, 5):
        try:
            # bot.remove_webhook()
            # bot.polling(none_stop=True)
            app.run(host=config['WEBHOOK_LISTEN'],
                    port=config['INTERNAL_PORT'])
            if bot.shutting_down:
                break
        except Exception as ex:
            o_logger.error(ex)
            util.log_error(ex)
            if not bot.error_msg:
                bot.error_msg = msg_to_owner(f"Бот упал, новая попытка ({i + 1}/5)")
            else:
                edit_message(f"Бот упал, новая попытка ({i + 1}/5)",
                             bot.error_msg.chat.id,
                             bot.error_msg.message_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', dest='debugging', action='store_true', help='Verbose output')
    args = parser.parse_args()
    try:
        main()
    except Exception as ex:
        util.log_error(ex)
