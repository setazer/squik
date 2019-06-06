# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#
# from bot_mng import bot, send_message, edit_message
# from config import config
# from db_mng import session_scope, User


# def save_users():
#     with session_scope() as session:
#         for user, userdata in bot.users.items():
#             db_user = User(user_id=user, access=userdata['access'], limit=userdata.get('limit', 0))
#             session.merge(db_user)


# def gen_user_markup(user):
#     user_markup = InlineKeyboardMarkup()
#     user_markup.row_width = 2
#     user_markup.add(InlineKeyboardButton("Да", callback_data=f"user_allow{user}"),
#                     InlineKeyboardButton("Нет", callback_data=f"user_deny{user}"))
#     user_markup.row(InlineKeyboardButton("Забанить", callback_data=f"user_block{user}"))
#     return user_markup
#
#
# @bot.message_handler(commands=['start'], func=lambda m: m.chat.type == "private")
# def start(message):
#     if message.chat.id not in bot.users:
#         send_message(message.chat.id, "Привет! Заявка на регистрацию отправлена администратору.")
#         send_message(config['OWNER_ID'],
#                      f"Новый пользователь: {message.from_user.username} ({message.chat.id})",
#                      reply_markup=gen_user_markup(message.chat.id))
#     elif bot.users[message.chat.id]['access'] == 1:
#         send_message(message.chat.id, "Регистрация уже пройдена.")
#
#     elif bot.users[message.chat.id]['access'] == 0:
#         send_message(message.chat.id, "Повторная заявка на регистрацию отправлена администратору.")
#         send_message(config['OWNER_ID'],
#                      f"Повторная регистрация: {message.from_user.username} ({message.chat.id})",
#                      reply_markup=gen_user_markup(message.chat.id))
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith('user_'))
# @bot.access(1)
# def callback_query(call):
#     if call.data.startswith("user_allow"):
#         user = int(call.data[len("user_allow"):])
#         bot.users[user]['access'] = 1
#         save_users()
#         send_message(user, "Регистрация подтверждена.")
#         edit_message(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Готово.")
#
#     elif call.data.startswith("user_deny"):
#         user = int(call.data[len("user_deny"):])
#         bot.users[user]['access'] = 0
#         save_users()
#         send_message(user, "Регистрация отклонена.")
#         edit_message(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Готово.")
#
#     elif call.data.startswith("user_block"):
#         user = int(call.data[len("user_block"):])
#         bot.users[user]['access'] = -1
#         save_users()
#         send_message(user, "Регистрация отклонена и заблокирована.")
