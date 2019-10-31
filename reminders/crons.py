import ast
import random
from datetime import datetime
from utils.database import execute_database_command
from bot import bot
from users.models import User


def remind_users(last_remind_utc):
    now_utc = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")  # TODO Нужно исправить
    reminders = execute_database_command('''SELECT user_id, mid FROM reminders 
    WHERE datetime_utc <= %s AND datetime_utc > %s;
    ''', (now_utc, last_remind_utc))
    for reminder in reminders:
        user_id, mid = reminder

        user = User.get(user_id)
        bot.send_message(user_id,
                         'Ты просил напомнить' if user.language_code == 'ru' else
                         'You asked to remind you')

        bot.forward_message(user_id, mid)

    return now_utc
