import datetime as dt
import time

import dateutil.relativedelta as rd

from bot_mng import bot, send_message


@bot.message_handler(commands=['uptime'], func=lambda m: m.chat.type == "private")
@bot.access(1)
def uptime(message, ):
    cur_time = dt.datetime.fromtimestamp(time.time())
    attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
    human_readable = lambda delta: [
        '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
        for attr in attrs if getattr(delta, attr)]
    diff = ' '.join(human_readable(rd.relativedelta(cur_time, bot.start_time)))
    send_message(message.chat.id, "Bot is running for: " + diff)
