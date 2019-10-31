from TamTamBot import CallbackButtonCmd
from openapi_client import Intent, RequestGeoLocationButton
from users.models import User
from checks.utils import CheckStatus
from users.data import preparing_habits


def get_menu_keyboard(user):
    ru_buttons = [
        [CallbackButtonCmd('🗓 Привычки', 'menu', {'section': 'habits'}, Intent.POSITIVE)],
        [CallbackButtonCmd('📝 Планы', 'menu', {'section': 'plans'}, Intent.POSITIVE)],
        [CallbackButtonCmd('🔔 Напомнинания 🆕', 'menu', {'section': 'reminders'}, Intent.POSITIVE)],
        [CallbackButtonCmd('⚙️ Настройки', 'menu', {'section': 'settings'}, Intent.POSITIVE)],
        [CallbackButtonCmd('✉️ Написать разработчикам', 'menu', {'section': 'contact_developers'}, Intent.POSITIVE)],
    ]

    en_buttons = [
        [CallbackButtonCmd('🗓 Habits', 'menu', {'section': 'habits'}, Intent.POSITIVE)],
        [CallbackButtonCmd('📝 Plans', 'menu', {'section': 'plans'}, Intent.POSITIVE)],
        [CallbackButtonCmd('🔔 Reminders 🆕', 'menu', {'section': 'reminders'}, Intent.POSITIVE)],
        [CallbackButtonCmd('⚙️ Settings', 'menu', {'section': 'settings'}, Intent.POSITIVE)],
        [CallbackButtonCmd('✉️ Contact developers', 'menu', {'section': 'contact_developers'}, Intent.POSITIVE)],
    ]

    buttons = ru_buttons if user.language_code == 'ru' else en_buttons

    return buttons


def get_habits_keyboard(user):
    ru_buttons = [
        [CallbackButtonCmd('🚴‍♂️ Активные', 'menu', {'section': 'active_habits'}, Intent.POSITIVE)],
        [CallbackButtonCmd('🎯 Новая привычка', 'new_habit', {}, Intent.POSITIVE)],
        [CallbackButtonCmd('✔️ Завершённые', 'menu', {'section': 'completed_habits'}, Intent.POSITIVE)],
        [CallbackButtonCmd('⬅ Назад', 'menu')],
    ]

    en_buttons = [
        [CallbackButtonCmd('🚴‍♂ Active', 'menu', {'section': 'active_habits'}, Intent.POSITIVE)],
        [CallbackButtonCmd('🎯 New habit', 'new_habit', {}, Intent.POSITIVE)],
        [CallbackButtonCmd('✔️ Completed', 'menu', {'section': 'completed_habits'}, Intent.POSITIVE)],
        [CallbackButtonCmd('⬅ Back', 'menu')],
    ]

    buttons = ru_buttons if user.language_code == 'ru' else en_buttons

    return buttons


def get_plans_keyboard(user):
    today_plan = user.today_plan
    if today_plan:
        today_plan_button = CallbackButtonCmd(
            'План на сегодня' if user.language_code == 'ru' else 'Today plan',
            'show_plan', {'plan_id': today_plan.id}, Intent.POSITIVE)
    else:
        today_plan_button = CallbackButtonCmd(
            'Составить план на сегодня' if user.language_code == 'ru' else 'Create today plan',
            'new_plan', {'day': 'today'}, Intent.POSITIVE)

    tomorrow_plan = user.tomorrow_plan
    if tomorrow_plan:
        tomorrow_plan_button = CallbackButtonCmd(
            'План на завтра' if user.language_code == 'ru' else 'Tomorrow plan',
            'show_plan', {'plan_id': tomorrow_plan.id}, Intent.POSITIVE)
    else:
        tomorrow_plan_button = CallbackButtonCmd(
            'Составить план на завтра' if user.language_code == 'ru' else 'Create tomorrow plan',
            'new_plan', {'day': 'tomorrow'}, Intent.POSITIVE)

    buttons = [
        [today_plan_button],
        [tomorrow_plan_button],
        [CallbackButtonCmd('⬅ Назад' if user.language_code == 'ru' else '⬅ Back', 'menu')],
    ]

    return buttons


def get_reminders_keyboard(user):
    ru_buttons = [
        [CallbackButtonCmd('🔔 Мои напоминания', 'menu', {'section': 'my_reminders'}, Intent.POSITIVE)],
        [CallbackButtonCmd('❓ Как создать напоминание', 'menu', {'section': 'reminders_help'}, Intent.POSITIVE)],
        [CallbackButtonCmd('⬅ Назад', 'menu')],
    ]

    en_buttons = [
        [CallbackButtonCmd('🔔 My reminders', 'menu', {'section': 'my_reminders'}, Intent.POSITIVE)],
        [CallbackButtonCmd('❓ How to create a reminder', 'menu', {'section': 'reminders_help'}, Intent.POSITIVE)],
        [CallbackButtonCmd('⬅ Back', 'menu')],
    ]

    buttons = ru_buttons if user.language_code == 'ru' else en_buttons

    return buttons


def get_settings_keyboard(user):
    ru_buttons = [
        [CallbackButtonCmd('🇷🇺 Язык', 'menu', {'section': 'language'}, Intent.POSITIVE)],
        [CallbackButtonCmd('🕒 Часовой пояс', 'menu', {'section': 'timezone'}, Intent.POSITIVE)],
        [CallbackButtonCmd('⬅ Назад', 'menu')],
    ]

    en_buttons = [
        [CallbackButtonCmd('🇬🇧 Language', 'menu', {'section': 'language'}, Intent.POSITIVE)],
        [CallbackButtonCmd('🕒 Timezone', 'menu', {'section': 'timezone'}, Intent.POSITIVE)],
        [CallbackButtonCmd('⬅ Back', 'menu')],
    ]

    buttons = ru_buttons if user.language_code == 'ru' else en_buttons

    return buttons


def get_language_keyboard(user):
    buttons = [
        [CallbackButtonCmd('🇷🇺Русский', 'menu',
                           {'section': 'language_change', 'language_code': 'ru'},
                           intent=Intent.POSITIVE),
         CallbackButtonCmd('🇬🇧English', 'menu',
                           {'section': 'language_change', 'language_code': 'en'},
                           intent=Intent.POSITIVE)],
        [CallbackButtonCmd('⬅ Назад' if user.language_code == 'ru' else '⬅ Back', 'menu')],
    ]

    return buttons


def get_timezone_keyboard(user):
    buttons = [
        [RequestGeoLocationButton(
            'Поделиться местоположением' if user.language_code == 'ru' else 'Share location',
            True)],
        [CallbackButtonCmd(
             '👆 Указать вручную' if user.language_code == 'ru' else '👆 Specify manually',
             'menu', {'section': 'pick_tz_menu'})],
    ]

    return buttons


def get_pick_tz_keyboard():
    buttons = [
        [CallbackButtonCmd('GMT', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT'})],

        [CallbackButtonCmd('GMT-0', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+0'}),
         CallbackButtonCmd('GMT+0', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-0'})],

        [CallbackButtonCmd('GMT-1', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+1'}),
         CallbackButtonCmd('GMT+1', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-1'})],

        [CallbackButtonCmd('GMT-2', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+2'}),
         CallbackButtonCmd('GMT+2', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-2'})],

        [CallbackButtonCmd('GMT-3', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+3'}),
         CallbackButtonCmd('GMT+3', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-3'})],

        [CallbackButtonCmd('GMT-4', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+4'}),
         CallbackButtonCmd('GMT+4', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-4'})],

        [CallbackButtonCmd('GMT-5', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+5'}),
         CallbackButtonCmd('GMT+5', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-5'})],

        [CallbackButtonCmd('GMT-6', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+6'}),
         CallbackButtonCmd('GMT+6', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-6'})],

        [CallbackButtonCmd('GMT-7', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+7'}),
         CallbackButtonCmd('GMT+7', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-7'})],

        [CallbackButtonCmd('GMT-8', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+8'}),
         CallbackButtonCmd('GMT+8', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-8'})],

        [CallbackButtonCmd('GMT-9', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+9'}),
         CallbackButtonCmd('GMT+9', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-9'})],

        [CallbackButtonCmd('GMT-10', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+10'}),
         CallbackButtonCmd('GMT+10', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-10'})],

        [CallbackButtonCmd('GMT-11', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+11'}),
         CallbackButtonCmd('GMT+11', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-11'})],

        [CallbackButtonCmd('GMT-12', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT+12'}),
         CallbackButtonCmd('GMT+12', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-12'})],

        [CallbackButtonCmd('GMT+13', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-13'})],

        [CallbackButtonCmd('GMT+14', 'menu', {'section': 'pick_tz', 'tz': 'Etc/GMT-14'})],
    ]

    return buttons


def get_delete_habit_keyboard(user, habit_id):
    button_label = 'Удалить' if user.language_code == 'ru' else 'Delete'

    buttons = [
        [CallbackButtonCmd(button_label, 'delete_habit', {'habit_id': habit_id}, Intent.NEGATIVE)],
    ]

    return buttons


def get_delete_reminder_keyboard(user, reminder_id):
    button_label = 'Удалить' if user.language_code == 'ru' else 'Delete'

    buttons = [
        [CallbackButtonCmd(button_label, 'delete_reminder', {'reminder_id': reminder_id}, Intent.NEGATIVE)],
    ]

    return buttons
