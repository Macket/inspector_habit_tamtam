from datetime import datetime
from tzwhere import tzwhere
import re
# import pytz
from menu.handlers import handle_main_menu
from users.utils import get_schedule
from checks.models import Check
from habits.models import Habit
from users.models import User
from users.data import preparing_habits
import users.keyboards as keyboards
from menu.keyboards import get_menu_keyboard


def register(bot, update):
    user = User(update.user_id,
                update.chat_id,
                username=update.user.username,
                first_name=update.user.name,
                timezone='UTC',
                )
    user.save()
    language_request(bot, update)


def language_request(bot, update):
    bot.send_message(update.user.user_id,
                     '🇷🇺 Выбери язык\n🇬🇧 Choose the language',
                     keyboard=keyboards.get_language_keyboard(),
                     update=update.update_current)


def language_response(bot, update):
    user = User.get(update.user_id)
    user.language_code = update.cmd_args['lang']
    user.save()
    language_confirm_request(bot, update)


def language_confirm_request(bot, update):
    lang_label = '🇷🇺Русский' if update.cmd_args['lang'] == 'ru' else '🇬🇧English'
    text = f'Ты уверен, что хочешь выбрать {lang_label}\n' \
           f'Are you sure you want to choose {lang_label}'

    bot.send_message(update.user_id,
                     text,
                     keyboard=keyboards.get_language_confirmation_keyboard(),
                     update=update.update_current)


def greeting_and_habit_request(bot, update):
    user = User.get(update.user_id)
    update.required_cmd_response = True
    ru_text = f'Привет{", " + user.first_name if user.first_name else ""}! ' \
              f'Я Инспектор Хэбит, борец с мировой ленью и прокрастинацией. ' \
              f'А ты, кажется, как раз испытваешь с этим определённые проблемы.\n\n' \
              f'Давай начнём бороться с этим прямо сейчас! ' \
              f'Отправь мне привычку, над которой хочешь работать.'

    en_text = f'Hello{", " + user.first_name if user.first_name else ""}! ' \
              f'I am Inspector Habit, the fighter with world laziness and procrastination. ' \
              f'And you seem to have trouble with it.\n\n' \
              f"Let's start fighting this right now! " \
              f"Send me the habit you want to work on."

    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id, text)


def habit_response(bot, update):
    user = User.get(update.user_id)

    ru_text = f'Итак, ты  хочешь\n\n*{update.message.body.text}*'
    en_text = f'So you want\n\n*{update.message.body.text}*'
    text = ru_text if user.language_code == 'ru' else en_text

    preparing_habits[update.user_id] = {'label': update.message.body.text, 'days_of_week': []}

    bot.send_message(update.user_id, text)
    days_request(bot, update)


def days_request(bot, update):
    user = User.get(update.user_id)

    ru_text = 'Теперь выбери дни недели, когда я буду приходить к тебе с проверкой.'
    en_text = "Now choose the days of the week when I will come to you with a check"
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id,
                     text,
                     keyboard=keyboards.get_days_keyboard(update.user_id))


def days_response(bot, update):
    selected_days = update.cmd_args['days_of_week']
    if len(selected_days) == 7:
        preparing_habits[update.user_id]['days_of_week'] = selected_days
    else:
        selected_day = selected_days[0]
        if selected_day in preparing_habits[update.user_id]['days_of_week']:
            preparing_habits[update.user_id]['days_of_week'].remove(selected_day)
        else:
            preparing_habits[update.user_id]['days_of_week'].append(selected_day)
            preparing_habits[update.user_id]['days_of_week'].sort()
    bot.send_message(update.user_id,
                     update.message.body.text,
                     keyboard=keyboards.get_days_keyboard(update.user_id),
                     update=update.update_current)


def time_request(bot, update):
    update.required_cmd_response = True
    user = User.get(update.user_id)

    ru_text = f'Отлично, выбери время проверки, например, *19:30*. ' \
              f'Можно выбрать несколько проверок через пробел, например, *7:30 19:30*'
    en_text = 'Good, choose a check time, for example, *19:30*. ' \
              'You can select multiple checks via space, for example, *7:30 19:30*'
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id, text)


def time_response(bot, update):
    user = User.get(update.user_id)
    ru_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    en_days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    days = ru_days if user.language_code == 'ru' else en_days

    time_array = update.message.body.text.split(' ')

    try:
        for time in time_array:
            timeformat = '%H:%M'
            datetime.strptime(time, timeformat)

        preparing_habits[update.user_id]['time_array'] = time_array
        check_days = re.sub(r'\s+', ' ', ' '.join(
            [day if day_of_week in preparing_habits[update.user_id]['days_of_week'] else '' for day_of_week, day in enumerate(days)])).strip()

        if user.timezone == 'UTC':
            ru_text = f'Хорошо, я буду проверять тебя в *{update.message.body.text}* по *{check_days}*.'
            en_text = f"Okay, I'll check you at *{update.message.body.text}* on *{check_days}*"
            text = ru_text if user.language_code == 'ru' else en_text

            bot.send_message(update.user_id, text)

            location_request(bot, update)
        else:
            habit_assign(bot, update)

    except ValueError:
        ru_text = 'Кажется, ты ввёл какую-то ерунду. Попробуй ещё раз, используя формат *ЧЧ:ММ*.'
        en_text = 'It seems you have entered some nonsense. Try again using *HH:MM* format.'
        text = ru_text if user.language_code == 'ru' else en_text

        bot.send_message(update.user_id, text, keyboard=keyboards.get_try_again_keyboard(user))


def location_request(bot, update):
    user = User.get(update.user_id)

    ru_text = 'Также мне нужно знать твой часовой пояс, чтобы проводить проверки вовремя.\n\n' \
              'Можешь просто поделиться местоположением или задать часовой пояс вручную.'
    en_text = 'I also need to find out what timezone you live in order to perform the checks on time.\n\n' \
              "You can just share location or specify timezone manually."
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user_id, text, keyboard=keyboards.get_location_keyboard(user))


def location_response(bot, update):
    tzw = tzwhere.tzwhere()
    latitude = update.message.body.attachments[0].latitude
    longitude = update.message.body.attachments[0].longitude
    timezone_str = tzw.tzNameAt(latitude, longitude)
    user = User.get(update.user_id)
    user.timezone = timezone_str
    user.save()


def timezone_request(bot, update):
    user = User.get(update.user_id)

    ru_text = 'Выбери свой часовой пояс'
    en_text = 'Choose your timezone'
    text = ru_text if user.language_code == 'ru' else en_text
    bot.send_message(update.user_id, text, keyboard=keyboards.get_timezone_keyboard(), update=update.update_current)


def timezone_response(bot, update):
    user = User.get(update.user_id)

    user.timezone = update.cmd_args['tz']
    user.save()


def habit_assign(bot, update):
    user = User.get(update.user_id)

    # Назначаем привычку
    habit = Habit(update.user_id,
                  preparing_habits[update.user_id]['label'],
                  preparing_habits[update.user_id]['days_of_week'],
                  preparing_habits[update.user_id]['time_array']).save()

    # Назначаем проверки
    schedule_native, schedule_utc = get_schedule(
        preparing_habits[update.user_id]['days_of_week'],
        preparing_habits[update.user_id]['time_array'],
        User.get(update.user_id).timezone,
    )

    for check_native, check_utc in zip(schedule_native, schedule_utc):  # TODO нужно оптимизировать
        Check(habit.id, check_native, check_utc).save()

    ru_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    en_days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    days = ru_days if user.language_code == 'ru' else en_days

    check_days = re.sub(r'\s+', ' ', ' '.join(
        [day if day_of_week in preparing_habits[update.user_id]['days_of_week'] else '' for day_of_week, day in
         enumerate(days)])).strip()
    check_time = ' '.join(preparing_habits[update.user_id]['time_array'])

    ru_text = f'Привычка *{habit.label}* сформирована.\n\n' \
              f'Дни недели: *{check_days}*\n' \
              f'Время проверки: *{check_time}*\n' \
              f'Длительность: *3 недели*\n\n' \
              f'Начинаем завтра!'
    en_text = f'The habit *{habit.label}* is formed.\n\n' \
              f'Days of week: *{check_days}*\n' \
              f'Checks time: *{check_time}*\n' \
              f'Duration: *3 weeks*\n\n' \
              f'We will start tomorrow!'
    text = ru_text if user.language_code == 'ru' else en_text

    del preparing_habits[update.user_id]

    bot.send_message(update.user_id, text)
    bot.send_sticker(update.user_id, 'ca3fe24b53')

    bot.send_message(update.user_id,
                     'Меню' if user.language_code == 'ru' else 'Menu',
                     keyboard=get_menu_keyboard(user))
