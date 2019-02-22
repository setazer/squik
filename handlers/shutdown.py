from flask import request

from bot_mng import bot, msg_to_owner
from db_mng import session_scope, Setting


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@bot.message_handler(commands=['shutdown'], func=lambda m: m.chat.type == "private")
@bot.access(2)
def shutdown(message):
    with session_scope() as session:
        last_shutdown = session.query(Setting).filter_by(setting='last_shutdown').first()
        if not last_shutdown:
            last_shutdown = '0_0'
        if last_shutdown == f'{message.chat.id}_{message.message_id}':
            return
        else:
            ls_setting = Setting(setting='last_shutdown', value=f'{message.chat.id}_{message.message_id}')
            session.merge(ls_setting)
    msg_to_owner("Останавливаюсь...")
    # shutdown_server()
    bot.stop_polling()
    bot.shutting_down = True
