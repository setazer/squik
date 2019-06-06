from bot_mng import bot, send_message


# from db_mng import session_scope, User


@bot.message_handler(commands=['broadcast'], func=lambda m: m.chat.type == "private")
@bot.access(2)
def broadcast_message(message):
    try:
        param = message.text.split()[1:]
    except IndexError:
        send_message(message.chat.id, text="А что передавать?")
        return
    msg = f"Сообщение от {message.from_user.username}:\n{' '.join(param)}"
    # with session_scope() as session:
    #     for user, in session.query(User.user_id).filter(User.access >= 1).all():
    #         if user != message.chat.id:
    for user in bot.users:
        send_message(user[''], msg)
    send_message(message.chat.id, text="Броадкаст отправлен.")
