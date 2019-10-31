from TamTamBot import CallbackButtonCmd
from openapi_client import Intent
from checks.utils import CheckStatus
from users.data import preparing_plans


def get_finish_plan_keyboard(user):
    buttons = [[CallbackButtonCmd(
        '❌ Отменить' if user.language_code == 'ru' else '❌ Cancel',
        'cancel_plan', {}, Intent.POSITIVE)]]
    if len(preparing_plans[user.id]['plan_array']) > 0:
        buttons.insert(0, [CallbackButtonCmd(
            'Завершить' if user.language_code == 'ru' else 'Finish',
            'finish_plan', {}, Intent.POSITIVE)])
    return buttons


def get_report_plan_keyboard(user, plan_id):
    return [[CallbackButtonCmd(
            'Отчитаться' if user.language_code == 'ru' else 'Report',
            'report_plan', {'plan_id': plan_id}, Intent.POSITIVE)],
            [CallbackButtonCmd(
                '⬅ Назад' if user.language_code == 'ru' else '⬅ Back',
                'menu', {'section': 'plans'})]]


def get_plan_item_keyboard(user, plan_id, item_idx, pending=True):
    if pending:
        done_label = '✔ Сделано' if user.language_code == 'ru' else '✔ Done'
        failed_label = '❌ Не сделано' if user.language_code == 'ru' else '❌ Failed'
        return [
            [CallbackButtonCmd('⬅️', 'plan_item_change', {'plan_id': plan_id, 'item_idx': item_idx, 'to': 'prev'}, Intent.POSITIVE),
             CallbackButtonCmd('➡️', 'plan_item_change', {'plan_id': plan_id, 'item_idx': item_idx, 'to': 'next'}, Intent.POSITIVE)],
            [CallbackButtonCmd(done_label, 'plan_item_report', {'plan_id': plan_id, 'item_idx': item_idx, 'status': CheckStatus.SUCCESS.value}, Intent.POSITIVE)],
            [CallbackButtonCmd(failed_label, 'plan_item_report', {'plan_id': plan_id, 'item_idx': item_idx, 'status': CheckStatus.FAIL.value}, Intent.POSITIVE)],
            [CallbackButtonCmd('⬅ Назад', 'show_plan', {'plan_id': plan_id})],
        ]
    else:
        return [
            [CallbackButtonCmd('⬅️', 'plan_item_change', {'plan_id': plan_id, 'item_idx': item_idx, 'to': 'prev'}, Intent.POSITIVE),
             CallbackButtonCmd('➡️', 'plan_item_change', {'plan_id': plan_id, 'item_idx': item_idx, 'to': 'next'}, Intent.POSITIVE)],
            [CallbackButtonCmd('⬅ Назад', 'show_plan', {'plan_id': plan_id})],
        ]
