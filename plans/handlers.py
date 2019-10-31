from users.models import User
from plans import keyboards
from users.data import preparing_plans
from plans.models import Plan
import datetime
import pytz
from checks.utils import CheckStatus, status_icons
from menu.handlers import handle_plans_menu


def handle_new_plan(bot, update):
    user = User.get(update.user_id)
    day_arg = update.cmd_args['day'] if update.cmd_args else 'today'
    if day_arg == 'today':
        day = datetime.datetime.now(tz=pytz.timezone(user.timezone)).date()  # today
    else:
        day = (datetime.datetime.now(tz=pytz.timezone(user.timezone)) + datetime.timedelta(1)).date()  # tomorrow

    preparing_plans[update.user_id] = {'update_current': update.update_current, 'plan_array': [], 'status_array': [], 'date': day}

    ru_text = 'Отправляй мне пункты плана по очереди, а я буду запоминать'
    en_text = 'Send me the plan items in turn, and I will remember'
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(update.user.user_id,
                     text,
                     keyboard=keyboards.get_finish_plan_keyboard(user),
                     update=update.update_current)


def handle_plan_append(bot, update):
    user = User.get(update.user_id)
    new_plan_item = update.message.body.text
    bot.delete_message(update.message.body.mid)
    preparing_plans[update.user_id]['plan_array'].append(new_plan_item)
    preparing_plans[update.user_id]['status_array'].append(CheckStatus.PENDING.value)

    plan_text = ""
    for num, item in enumerate(preparing_plans[update.user_id]['plan_array'], 1):
        plan_text += f'{num}. {item}\n'

    bot.send_message(update.user.user_id,
                     plan_text,
                     keyboard=keyboards.get_finish_plan_keyboard(user),
                     update=preparing_plans[update.user_id]['update_current'])


def handle_finish_plan(bot, update):
    user = User.get(update.user_id)
    plan = Plan(update.user_id,
                preparing_plans[update.user_id]['plan_array'],
                preparing_plans[update.user_id]['status_array'],
                preparing_plans[update.user_id]['date']).save()

    today = datetime.datetime.now(tz=pytz.timezone(user.timezone)).date()
    if today == plan.date:
        plan_text = "*План на сегодня*\n\n" if user.language_code == 'ru' else '*Plan for today*\n\n'
    else:
        plan_text = "*План на завтра*\n\n" if user.language_code == 'ru' else '*Plan for tomorrow*\n\n'

    for num, item in enumerate(plan.plan_array, 1):
        plan_text += f'🔲 {item}\n'

    bot.send_message(update.user_id,
                     plan_text,
                     keyboard=keyboards.get_report_plan_keyboard(user, plan_id=plan.id),
                     update=preparing_plans[update.user_id]['update_current'])

    del preparing_plans[update.user_id]


def handle_cancel_plan(bot, update):
    del preparing_plans[update.user_id]
    handle_plans_menu(bot, update)


def handle_report_plan(bot, update):
    user = User.get(update.user_id)
    plan = Plan.get(update.cmd_args['plan_id'])
    text = f'{status_icons[plan.status_array[0]]} {plan.plan_array[0]}'

    bot.send_message(update.user_id,
                     text,
                     keyboard=keyboards.get_plan_item_keyboard(user, plan.id, 0, pending=plan.status_array[0] == CheckStatus.PENDING.value),
                     update=update.update_current)


def handle_plan_item_change(bot, update):
    user = User.get(update.user_id)
    plan = Plan.get(update.cmd_args['plan_id'])
    cur_item_idx = update.cmd_args['item_idx']
    new_item_dx = ((cur_item_idx + 1) % len(plan.plan_array)) if update.cmd_args['to'] == 'next' \
        else ((cur_item_idx - 1) % len(plan.plan_array))
    text = f'{status_icons[plan.status_array[new_item_dx]]} {plan.plan_array[new_item_dx]}'

    bot.send_message(update.user_id,
                     text,
                     keyboard=keyboards.get_plan_item_keyboard(
                         user, plan.id, new_item_dx, pending=plan.status_array[new_item_dx] == CheckStatus.PENDING.value),
                     update=update.update_current)


def handle_show_plan(bot, update):
    user = User.get(update.user_id)
    if update.cmd_args:
        plan = Plan.get(update.cmd_args['plan_id'])
    else:
        plan = user.today_plan

    today = datetime.datetime.now(tz=pytz.timezone(user.timezone)).date()
    if today == plan.date:
        plan_text = "*План на сегодня*\n\n" if user.language_code == 'ru' else '*Plan for today*\n\n'
    else:
        plan_text = "*План на завтра*\n\n" if user.language_code == 'ru' else '*Plan for tomorrow*\n\n'

    for item, status in zip(plan.plan_array, plan.status_array):
        plan_text += f'{status_icons[status]} {item}\n'

    if CheckStatus.PENDING.value in plan.status_array:
        bot.send_message(update.user.user_id,
                         plan_text,
                         keyboard=keyboards.get_report_plan_keyboard(user, plan.id),
                         update=update.update_current)
    else:
        bot.send_message(update.user.user_id, plan_text)


def handle_today_plan(bot, update):
    user = User.get(update.user_id)
    if user.today_plan:
        handle_show_plan(bot, update)
    else:
        ru_text = 'План на сегодня ещё не составлен. Самое время сделать это!😊'
        en_text = "The plan for today has not yet been drawn up. It's time to do it!😊"
        text = ru_text if user.language_code == 'ru' else en_text

        bot.send_message(update.user_id, text)
        handle_plans_menu(bot, update)


def handle_plan_item_report(bot, update):
    user = User.get(update.user_id)
    plan = Plan.get(update.cmd_args['plan_id'])
    item_idx = update.cmd_args['item_idx']
    status = update.cmd_args['status']
    plan.status_array[item_idx] = status
    plan.save()

    if status == CheckStatus.SUCCESS.value:
        user.score += 1
    elif status == CheckStatus.FAIL.value:
        user.score -= 1
    user.save()

    if CheckStatus.PENDING.value in plan.status_array:
        text = f"{status_icons[status]} {plan.plan_array[item_idx]}\n\n"
        sign = '+' if status == CheckStatus.SUCCESS.value else '-'
        point = '1 очко' if user.language_code == 'ru' else '1 point'
        text += sign + point

        bot.send_message(update.user_id,
                         text,
                         keyboard=keyboards.get_plan_item_keyboard(
                             user, plan.id, item_idx, pending=(status == CheckStatus.PENDING.value)),
                         update=update.update_current)
        return False

    else:
        handle_show_plan(bot, update)
        ru_text = 'Теперь можно и отдохнуть😊'
        en_text = 'Now you can relax😊'
        text = ru_text if user.language_code == 'ru' else en_text

        bot.send_message(update.user_id, text)
        return True
