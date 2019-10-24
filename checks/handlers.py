import ast
import random
from datetime import datetime
from utils.database import execute_database_command
# from bot import bot
from users.models import User
from checks.models import Check
from habits.models import Habit
from checks.utils import CheckStatus
from checks import keyboards
from users.utils import get_user_naming

success_stickers = ['c22ed421f4',
                    'cfb940b253',
                    'cf8c068053',
                    'cf9602fc53',
                    'cf2d68e853',
                    'cf8c68ae53',
                    'cf345c1353',
                    'cec71e0953',
                    'cec71dce53',
                    'cf301ab453',
                    'ce43d55f53',
                    'ce43d4bf53',
                    'cf2d690b53',
                    'cc028a1253',
                    'cb84872953',
                    'cb84841b53',
                    'ce92223000']

fail_stickers = ['cf8c68ce53',
                 'cec71fe753',
                 'cf30017153',
                 'cec964a553',
                 'cd88e15f53',
                 'cb8492c753',
                 'cdf2b51a53',
                 'cd896dd253',
                 'c88d1c1597',
                 'c2d91ba447',
                 'c2a8377fbb',
                 'cfb941e953',
                 'cfa8575953',
                 'cf96056953',
                 'cf3002c653',
                 'cec6ae4847',
                 'cea78eab53',
                 'cdd850c153',
                 'cb8490fb53',
                 'ca41ba0d53']


def handle_habit_report(bot, update):
    check = Check.get(update.cmd_args['check_id'])
    check.status = update.cmd_args['status']
    check.save()

    habit = Habit.get(check.habit_id)

    user = User.get(update.user_id)

    if update.cmd_args['status'] == CheckStatus.SUCCESS.name:
        bot.send_sticker(update.user_id, random.choice(success_stickers))
        bot.send_message(update.user_id, '+1 очко' if user.language_code == 'ru' else '+1 point')
        user.score += 1  # TODO Заменить на последовательность
        user.save()
    else:
        bot.send_sticker(update.user_id, random.choice(fail_stickers))
        bot.send_message(update.user_id, '-1 очко' if user.language_code == 'ru' else '-1 point')
        user.score -= 1  # TODO Заменить на последовательность
        user.save()

    if not habit.get_remaining_checks():
        suggest_new_habit(bot, user, habit)


def suggest_new_habit(bot, user, old_habit):
    ru_text = f'Ты завершил работу над привычкой *{old_habit.label}*. ' \
              f'Пора назначить новую!'
    en_text = f'You finished the habit *{old_habit.label}*. ' \
              f"It's time to assign the new one!"
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(user.id, text, keyboard=keyboards.get_new_habit_keyboard(user))  # TODO Добавить keyboard
