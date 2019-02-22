from bot_mng import bot, send_message, msg_to_owner
from db_mng import session_scope, User


def save_users():
    with session_scope() as session:
        for user, userdata in bot.users.items():
            db_user = User(user_id=user, access=userdata['access'], limit=userdata.get('limit', 0))
            session.merge(db_user)


@bot.message_handler(commands=['stop'], func=lambda m: m.chat.type == "private")
@bot.access(1)
def stop(message):
    send_message(message.chat.id, "Регистрация отозвана.")
    msg_to_owner(f"Регистрация {message.from_user.username} ({message.chat.id}) отозвана.")
    bot.users[message.chat.id]['access'] = 0
    save_users()
