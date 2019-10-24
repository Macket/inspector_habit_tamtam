from TamTamBot import CallbackButtonCmd
from openapi_client import Intent, RequestGeoLocationButton
from users.models import User
from checks.utils import CheckStatus
from users.data import preparing_habits


def get_check_keyboard(user, check_id):
    buttons = [
        [CallbackButtonCmd(
            '✔️ Да' if user.language_code == 'ru' else '✅ Yes', 'habit_report',
            {'check_id': check_id, 'status': CheckStatus.SUCCESS.name},
            intent=Intent.POSITIVE),
         CallbackButtonCmd(
             '❌ Нет' if user.language_code == 'ru' else '❌ No', 'habit_report',
             {'check_id': check_id, 'status': CheckStatus.FAIL.name},
             intent=Intent.POSITIVE)],
    ]

    return buttons


def get_new_habit_keyboard(user):
    ru_buttons = [
        [CallbackButtonCmd('🎯 Новая привычка', 'new_habit', {}, Intent.POSITIVE)],
    ]

    en_buttons = [
        [CallbackButtonCmd('🎯 New habit', 'new_habit', {}, Intent.POSITIVE)],
    ]

    buttons = ru_buttons if user.language_code == 'ru' else en_buttons

    return buttons
