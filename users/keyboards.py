from TamTamBot import CallbackButtonCmd
from openapi_client import Intent, RequestGeoLocationButton
from users.models import User
from users.data import preparing_habits


def get_language_keyboard():
    buttons = [
        [CallbackButtonCmd('🇷🇺Русский', 'set_lang', {'lang': 'ru'}, intent=Intent.POSITIVE),
         CallbackButtonCmd('🇬🇧English', 'set_lang', {'lang': 'en'}, intent=Intent.POSITIVE)],
    ]

    return buttons


def get_language_confirmation_keyboard():
    buttons = [
        [CallbackButtonCmd('Да / Yes', 'greeting', intent=Intent.POSITIVE),
         CallbackButtonCmd('Нет / No', 'set_lang', intent=Intent.POSITIVE)],
    ]

    return buttons


def get_days_keyboard(user_id):
    user = User.get(user_id)
    ru_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    en_days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    days = ru_days if user.language_code == 'ru' else en_days

    buttons = [
        [CallbackButtonCmd(
            '✔️' + day if day_of_week in preparing_habits[user_id]['days_of_week'] else day,
            'pick_days',
            {'days_of_week': [day_of_week]}) for day_of_week, day in enumerate(days[:4])],
        [CallbackButtonCmd(
            '✔️' + day if day_of_week + 4 in preparing_habits[user_id]['days_of_week'] else day,
            'pick_days',
            {'days_of_week': [day_of_week + 4]}) for day_of_week, day in enumerate(days[4:])],
        [CallbackButtonCmd(
            'Все' if user.language_code == 'ru' else 'All',
            'pick_days',
            {'days_of_week': [0, 1, 2, 3, 4, 5, 6]})]
    ]

    if len(preparing_habits[user_id]['days_of_week']) > 0:
        buttons.append(
            [CallbackButtonCmd('Готово' if user.language_code == 'ru' else 'Done',
                               'pick_time', intent=Intent.POSITIVE)]
        )

    return buttons


def get_try_again_keyboard(user):
    return [
        [CallbackButtonCmd(
            'Попробовать ещё раз' if user.language_code == 'ru' else 'Try again',
            'pick_time', intent=Intent.POSITIVE)
        ]]


def get_location_keyboard(user):
    buttons = [
        [RequestGeoLocationButton(
            'Поделиться местоположением' if user.language_code == 'ru' else 'Share location',
            True)],
         [CallbackButtonCmd(
             'Указать вручную' if user.language_code == 'ru' else 'Specify manually',
             'pick_tz')],
    ]

    return buttons


def get_timezone_keyboard():
    buttons = [
        [CallbackButtonCmd('GMT', 'pick_tz', {'tz': 'Etc/GMT'})],

        [CallbackButtonCmd('GMT-0', 'pick_tz', {'tz': 'Etc/GMT+0'}),
         CallbackButtonCmd('GMT+0', 'pick_tz', {'tz': 'Etc/GMT-0'})],

        [CallbackButtonCmd('GMT-1', 'pick_tz', {'tz': 'Etc/GMT+1'}),
         CallbackButtonCmd('GMT+1', 'pick_tz', {'tz': 'Etc/GMT-1'})],

        [CallbackButtonCmd('GMT-2', 'pick_tz', {'tz': 'Etc/GMT+2'}),
         CallbackButtonCmd('GMT+2', 'pick_tz', {'tz': 'Etc/GMT-2'})],

        [CallbackButtonCmd('GMT-3', 'pick_tz', {'tz': 'Etc/GMT+3'}),
         CallbackButtonCmd('GMT+3', 'pick_tz', {'tz': 'Etc/GMT-3'})],

        [CallbackButtonCmd('GMT-4', 'pick_tz', {'tz': 'Etc/GMT+4'}),
         CallbackButtonCmd('GMT+4', 'pick_tz', {'tz': 'Etc/GMT-4'})],

        [CallbackButtonCmd('GMT-5', 'pick_tz', {'tz': 'Etc/GMT+5'}),
         CallbackButtonCmd('GMT+5', 'pick_tz', {'tz': 'Etc/GMT-5'})],

        [CallbackButtonCmd('GMT-6', 'pick_tz', {'tz': 'Etc/GMT+6'}),
         CallbackButtonCmd('GMT+6', 'pick_tz', {'tz': 'Etc/GMT-6'})],

        [CallbackButtonCmd('GMT-7', 'pick_tz', {'tz': 'Etc/GMT+7'}),
         CallbackButtonCmd('GMT+7', 'pick_tz', {'tz': 'Etc/GMT-7'})],

        [CallbackButtonCmd('GMT-8', 'pick_tz', {'tz': 'Etc/GMT+8'}),
         CallbackButtonCmd('GMT+8', 'pick_tz', {'tz': 'Etc/GMT-8'})],

        [CallbackButtonCmd('GMT-9', 'pick_tz', {'tz': 'Etc/GMT+9'}),
         CallbackButtonCmd('GMT+9', 'pick_tz', {'tz': 'Etc/GMT-9'})],

        [CallbackButtonCmd('GMT-10', 'pick_tz', {'tz': 'Etc/GMT+10'}),
         CallbackButtonCmd('GMT+10', 'pick_tz', {'tz': 'Etc/GMT-10'})],

        [CallbackButtonCmd('GMT-11', 'pick_tz', {'tz': 'Etc/GMT+11'}),
         CallbackButtonCmd('GMT+11', 'pick_tz', {'tz': 'Etc/GMT-11'})],

        [CallbackButtonCmd('GMT-12', 'pick_tz', {'tz': 'Etc/GMT+12'}),
         CallbackButtonCmd('GMT+12', 'pick_tz', {'tz': 'Etc/GMT-12'})],

        [CallbackButtonCmd('GMT+13', 'pick_tz', {'tz': 'Etc/GMT-13'})],

        [CallbackButtonCmd('GMT+14', 'pick_tz', {'tz': 'Etc/GMT-14'})],
    ]

    return buttons
