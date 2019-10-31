from users.models import User
from checks.models import Check
from habits.models import Habit
from reminders.models import Reminder
from checks.utils import status_icons
from menu import keyboards
from users.utils import get_user_naming
from utils.database import execute_database_command
import settings
from tzwhere import tzwhere
import re
from datetime import datetime


def handle_main_menu(bot, update):
    user = User.get(update.user_id)

    bot.send_message(update.user_id,
                     'Меню' if user.language_code == 'ru' else 'Menu',
                     keyboard=keyboards.get_menu_keyboard(user),
                     update=update.update_current)


def handle_habits_menu(bot, update):
    user = User.get(update.user_id)

    bot.send_message(update.user.user_id,
                     'Привычки' if user.language_code == 'ru' else 'Habits',
                     keyboard=keyboards.get_habits_keyboard(user),
                     update=update.update_current)


def handle_plans_menu(bot, update):
    user = User.get(update.user_id)

    bot.send_message(update.user.user_id,
                     'Планы' if user.language_code == 'ru' else 'Plans',
                     keyboard=keyboards.get_plans_keyboard(user),
                     update=update.update_current)


def handle_reminders_menu(bot, update):
    user = User.get(update.user_id)

    bot.send_message(update.user.user_id,
                     'Напоминания' if user.language_code == 'ru' else 'Reminders',
                     keyboard=keyboards.get_reminders_keyboard(user),
                     update=update.update_current)


def handle_settings_menu(bot, update):
    user = User.get(update.user_id)

    bot.send_message(update.user.user_id,
                     'Настройки' if user.language_code == 'ru' else 'Settings',
                     keyboard=keyboards.get_settings_keyboard(user),
                     update=update.update_current)


def handle_contact_developers(bot, update):
    user = User.get(update.user_id)

    ru_text = 'Напиши сообщение моим разработчикам или отправь *Отмена*'
    en_text = 'Write the message to my developers or send *Cancel*'
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user.user_id, text)


def handle_send_feedback(bot, update):
    user = User.get(update.user_id)
    feedback = f'id: {user.id}\n' \
               f'Пользователь: {user.username}\n' \
               f'Имя: {user.first_name}\n' \
               f'Фамилия: {user.last_name}\n' \
               f'Язык: {user.language_code}\n\n' \
               f'Сообщение: *{update.message.body.text}*'
    bot.send_message(settings.ADMIN_ID, feedback)

    ru_text = 'Твоё сообщение успешно отправлено😉'
    en_text = "Your message has been successfully sent😉"
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id, text)


def handle_language_menu(bot, update):
    user = User.get(update.user_id)

    bot.send_message(update.user_id,
                     'Выбери язык' if user.language_code == 'ru' else 'Choose the language',
                     keyboard=keyboards.get_language_keyboard(user),
                     update=update.update_current)


def handle_language_change(bot, update):
    user = User.get(update.user_id)
    user.language_code = update.cmd_args['language_code']
    user.save()

    ru_text = 'Язык изменён на *Русский*'
    en_text = 'Language changed to *English*'
    text = ru_text if user.language_code == 'ru' else en_text
    bot.send_message(update.user_id, text)


def handle_timezone_menu(bot, update):
    user = User.get(update.user_id)

    ru_text = "Можно просто поделиться местоположением или задать часовой пояс вручную"
    en_text = "You can just share location or specify timezone manually"
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id,
                     text,
                     keyboard=keyboards.get_timezone_keyboard(user),
                     update=update.update_current)


def handle_pick_tz_menu(bot, update):
    user = User.get(update.user_id)

    ru_text = "Выбери свой часовой пояс"
    en_text = "Choose your timezone"
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id,
                     text,
                     keyboard=keyboards.get_pick_tz_keyboard(),
                     update=update.update_current)


def handle_pick_tz(bot, update):
    user = User.get(update.user_id)

    user.timezone = update.cmd_args['tz']
    user.save()

    tz_str = update.cmd_args['tz'][4:]
    tz_str = tz_str.replace('-', '+') if '-' in tz_str else tz_str.replace('+', '-')
    ru_text = f'Часовой пояс изменён на *{tz_str}*.\n\n' \
              f'Обрати внимание, что проверки по уже назначенным привычкам ' \
              f'будут происходить по старому часовому поясу.'
    en_text = f'Timezone changed to *{tz_str}*.\n\n' \
              f'Please note that checks for already assigned habits ' \
              f'will occur in the old timezone.'
    text = ru_text if user.language_code == 'ru' else en_text
    bot.send_message(update.user_id, text)


def handle_location(bot, update):
    tzw = tzwhere.tzwhere()
    latitude = update.message.body.attachments[0].latitude
    longitude = update.message.body.attachments[0].longitude
    tz_str = tzw.tzNameAt(latitude, longitude)
    user = User.get(update.user_id)
    user.timezone = tz_str
    user.save()

    ru_text = f'Часовой пояс изменён на *{tz_str}*'
    en_text = f'Timezone changed to *{tz_str}*'
    text = ru_text if user.language_code == 'ru' else en_text
    bot.send_message(update.user_id, text)


def handle_completed_habits(bot, update):
    habit_ids = execute_database_command(
        f'SELECT id FROM habits WHERE user_id = {update.user_id}')
    completed_habits_report = {}
    for habit_id in habit_ids:
        habit_id = habit_id[0]
        habit = Habit.get(habit_id)
        if not habit.get_remaining_checks():
            check_statuses = execute_database_command(
                f'SELECT status FROM checks WHERE habit_id = {habit_id} ORDER BY datetime_utc;')

            for check_status in check_statuses:
                check_status = check_status[0]
                if habit_id in completed_habits_report:
                    completed_habits_report[habit_id]['checks'].append(status_icons[check_status])
                else:
                    completed_habits_report[habit_id] = \
                        {'label': habit.label, 'checks': [status_icons[check_status]]}

    if completed_habits_report:
        report = ''
        for habit in completed_habits_report.values():
            report += f'*{habit["label"]}*\n{" ".join(habit["checks"])}\n\n'
    else:
        user = User.get(update.user_id)
        ru_report = 'Нет ни одной завершённой привычки'
        en_report = 'There are no completed habits'
        report = ru_report if user.language_code == 'ru' else en_report

    bot.send_message(update.user_id, report)


def handle_active_habits(bot, update):
    user = User.get(update.user_id)
    habit_ids = execute_database_command(
        f'SELECT id FROM habits WHERE user_id = {user.id}')

    active_habits_ids = []
    for habit_id in habit_ids:
        habit_id = habit_id[0]
        habit = Habit.get(habit_id)
        if habit.get_remaining_checks():
            active_habits_ids.append(habit_id)
            check_statuses = execute_database_command(
                f'SELECT status FROM checks WHERE habit_id = {habit_id} ORDER BY datetime_utc;')

            check_report = ''
            for check_status in check_statuses:
                check_report += status_icons[check_status[0]]

            # TODO убрать дублирование кода с Intro
            ru_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
            en_days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
            days = ru_days if user.language_code == 'ru' else en_days

            days_of_week = list(map(lambda x: int(x), habit.days_of_week[1:-1].split(',')))
            time_array = list(map(lambda x: x.strip(), habit.time_array[1:-1].split(',')))
            check_days = re.sub(r'\s+', ' ', ' '.join(
                [day if day_of_week in days_of_week else '' for day_of_week, day in
                 enumerate(days)])).strip()
            check_time = ' '.join(time_array)

            ru_text = f'Привычка: *{habit.label}*\n' \
                      f'Дни недели: *{check_days}*\n' \
                      f'Время проверки: *{check_time}*\n' \
                      f'Длительность: *3 недели*\n\n' \
                      f'Прогресс\n'
            en_text = f'Habit: *{habit.label}*\n' \
                      f'Days of week: *{check_days}*\n' \
                      f'Checks time: *{check_time}*\n' \
                      f'Duration: *3 weeks*\n\n' \
                      f'Progress\n'
            text = ru_text if user.language_code == 'ru' else en_text

            text += check_report

            bot.send_message(update.user_id, text, keyboard=keyboards.get_delete_habit_keyboard(user, habit_id))

    if not active_habits_ids:
        ru_text = 'Нет ни одной активной привычки'
        en_text = 'There are no active habits'
        text = ru_text if user.language_code == 'ru' else en_text
        bot.send_message(update.user_id, text)


def handle_delete_habit(bot, update):
    user = User.get(update.user_id)
    habit = Habit.get(update.cmd_args['habit_id'])
    if habit:
        execute_database_command(f'DELETE FROM habits WHERE id = {habit.id};')
        ru_text = f'Привычка *{habit.label}* удалена'
        en_text = f'The habit *{habit.label}* has been deleted'
        text = ru_text if user.language_code == 'ru' else en_text
    else:
        ru_text = f'Такой привычки не существует'
        en_text = f'This habit does not exists'
        text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id, text)


def handle_delete_reminder(bot, update):
    user = User.get(update.user_id)
    reminder = Reminder.get(update.cmd_args['reminder_id'])
    if reminder:
        execute_database_command(f'DELETE FROM reminders WHERE id = {reminder.id};')
        bot.delete_message(update.message.body.mid)
    else:
        ru_text = f'Такого напоминания не существует'
        en_text = f'This reminder does not exists'
        text = ru_text if user.language_code == 'ru' else en_text

        bot.send_message(update.user_id, text)


def handle_new_habit(bot, update):
    update.required_cmd_response = True

    user = User.get(update.user_id)

    ru_text = 'Над какой привычкой будем работать?'
    en_text = 'What habit will we work on?'
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id, text)


def handle_my_reminders(bot, update):
    user = User.get(update.user_id)
    now_utc = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")  # TODO Нужно исправить
    reminders = execute_database_command(
        f'SELECT id, mid, datetime_native FROM reminders WHERE '
        f'datetime_utc > %s AND user_id = %s', (now_utc, user.id))

    for reminder in reminders:
        reminder_id = reminder[0]
        mid = reminder[1]
        date = reminder[2].strftime("%d.%m.%Y")
        time = reminder[2].strftime("%H:%M")
        print(reminder_id)
        text = f'{date} в {time}'
        if user.language_code != 'ru':
            text = 'On ' + text.replace('в', 'at')
        bot.reply_message(user.id, mid, text, keyboard=keyboards.get_delete_reminder_keyboard(user, reminder_id))

    if not reminders:
        ru_text = 'Нет ни одного напоминания'
        en_text = 'There are no any reminders'
        text = ru_text if user.language_code == 'ru' else en_text
        bot.send_message(update.user_id, text)


def handle_reminders_help(bot, update):
    user = User.get(update.user_id)
    ru_text = 'Чтобы создать напоминание, отправь мне голосовое сообщение следующего плана: ' \
              '*Напомни мне ... <сегодня|завтра|день недели> в <время>*\n\n' \
              'Например:\n' \
              '*Напомни мне позвонить маме сегодня в двадцать тридцать (20:30)*\n' \
              '*Напомни мне убраться в воскресенье в двенадцать ноль ноль (12:00)*\n\n' \
              'Порядок слов не важен. Главное, чтобы были указаны день и время.'
    en_text = 'To create a reminder send me the voice message such as: ' \
              'Remind me ... <today|tomorrow|day of week> at <time>\n\n' \
              'For example:\n' \
              '*Remind me to call my mother today at three ought seven p m (15:07)*\n' \
              '*Remind me to clean my room on sunday at ten a m (10:00)*\n\n' \
              "The order of words doesn't matter. The main thing is that a day and time are indicated."
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id, text)
