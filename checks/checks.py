import ast
import random
from datetime import datetime
from utils.database import execute_database_command
from bot import bot
from users.models import User
from checks.models import Check
from habits.models import Habit
from checks.utils import CheckStatus
from checks import keyboards
from users.utils import get_user_naming


def check_users(last_check_utc):
    now_utc = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")  # TODO Нужно исправить
    checks = execute_database_command('''SELECT c.id, c.habit_id, c.datetime_native, c.datetime_utc, h.label, h.user_id FROM
    checks c JOIN habits h ON c.habit_id = h.id JOIN users u ON u.id = h.user_id 
    WHERE c.datetime_utc <= %s AND c.datetime_utc > %s AND c.status=%s;
    ''', (now_utc, last_check_utc, CheckStatus.PENDING.name))
    for check in checks:
        check_id, habit_id, datetime_native, datetime_utc, label, user_id = check
        c = Check(habit_id, datetime_native, datetime_utc, CheckStatus.CHECKING.name, check_id)
        c.save()

        user = User.get(user_id)
        ru_text = f'Ты обещал *{label}*. Ты держишь своё слово?'
        en_text = f'You promised *{label}*. Are you keeping your promise?'
        text = ru_text if user.language_code == 'ru' else en_text

        bot.send_message(user_id,
                         text,
                         keyboard=keyboards.get_check_keyboard(user, check_id))

    return now_utc


def rate_users():
    rating = execute_database_command(
        'SELECT id, score FROM users ORDER BY score DESC;',
        (CheckStatus.SUCCESS.name,))

    total = len(rating)

    for place, record in enumerate(rating, 1):
        u = User.get(record[0])

        ru_text = f'Твоё место в рейтинге: *{place}/{total}*\n\n' \
                  f'Количество очков: *{record[1]}*'
        en_text = f'Your place in rating *{place}/{total}*\n\n' \
                  f'Score: *{record[1]}*'
        text = ru_text if u.language_code == 'ru' else en_text

        bot.send_message(u.id, text)


# Jason_Statham_sticker_pack = ['CAADBAADiAIAAoVpUQWeomfO2K5XagI',
#                               'CAADBAADuQIAAoVpUQVxWNshtJbFxwI',
#                               'CAADBAADjgIAAoVpUQWFTHDH5-5gLQI',
#                               'CAADBAADkwIAAoVpUQUWaJtDeSffxQI',
#                               'CAADBAADlQIAAoVpUQXTjabcb8sc5QI',
#                               'CAADBAADlwIAAoVpUQU_mDUvVNQrCgI',
#                               'CAADBAADnQIAAoVpUQUzSVrPUoUblQI',
#                               'CAADBAADnwIAAoVpUQUv6h29VDUm0wI',
#                               'CAADBAADoQIAAoVpUQUp6ATKJ0CCwgI',
#                               'CAADBAADowIAAoVpUQUe179jKBFMmAI',
#                               'CAADBAADpQIAAoVpUQX5pkA5Un8m9gI',
#                               'CAADBAADpwIAAoVpUQULoMsJeHJ5dQI',
#                               'CAADBAADqQIAAoVpUQV8lGGpxy7bLwI',
#                               'CAADBAADqwIAAoVpUQVnjHeRzWVcfgI',
#                               'CAADBAADrQIAAoVpUQWCbdLOmJiC2wI',
#                               'CAADBAADrwIAAoVpUQWj5VIseT0VmwI',
#                               'CAADBAADsQIAAoVpUQXeqyOsHpec8wI',
#                               'CAADBAADswIAAoVpUQWZdNjc6_LJNwI',
#                               'CAADBAADtQIAAoVpUQWcyMnP-eLZdgI',
#                               'CAADBAADtwIAAoVpUQWPap6lxRn7lgI',
#                               'CAADBAADuwIAAoVpUQWQWheljG3tRQI']
#
# Jason_Statham_quotes_ru = ['В любом процессе важна не скорость, а удовольствие.',
#                            'Не так важно, как тебя ударили, - важно, как ты встал и ответил.',
#                            'Если стараться обходить все неприятности, то можно пройти мимо всех удовольствий.',
#                            'Ты свободен, а значит, всерьёз за себя отвечаешь.',
#                            'Молчание - лучший способ ответа на бессмысленные вопросы.',
#                            'Тем, кого вдохновляют мои герои, не помешало бы лишний раз подумать.',
#                            'Живи в свое удовольствие, но не забывай про тех кто рядом.',
#                            'Будь самим собой, имей свою точку зрения, умей постоять за себя и за своих близких и тебя будут уважать.',
#                            'У тебя есть враги? Хорошо. Значит, в своей жизни ты что-то когда-то отстаивал.',
#                            'Если вы идете сквозь ад — идите, не останавливаясь.',
#                            'Умный человек не делает сам все ошибки — он дает шанс и другим.',
#                            'Любой кризис — это новые возможности.',
#                            'Успех — это способность шагать от одной неудачи к другой, не теряя энтузиазма.',
#                            'Сокол высоко поднимается, когда летит против ветра, а не по ветру.',
#                            'Глуп тот человек, который никогда не меняет своего мнения.',
#                            'Когда орлы молчат, болтают попугаи.',
#                            'На протяжении своей жизни каждому человеку доводится споткнуться о свой «великий шанс». К несчастью, большинство из нас просто подымается, отряхивается и идет дальше, как будто ничего и не произошло.',
#                            'Не желайте здоровья и богатства, а желайте удачи, ибо на Титанике все были богаты и здоровы, а удачливыми оказались единицы!',
#                            'Ложь успевает обойти полмира, пока правда одевает штаны.',
#                            'Хотите, чтобы в споре ваше слово было последним? Скажите оппоненту «Пожалуй, Вы правы».',
#                            'Мои вкусы просты. Я легко удовлетворяюсь наилучшим.',
#                            'Большое преимущество получает тот, кто достаточно рано сделал ошибки, на которых можно учиться.',
#                            'Величайший урок жизни в том, что и дураки бывают правы.',
#                            'Мы живем в эпоху больших событий и маленьких людей.',
#                            'От деревянных башмаков к деревянным башмакам — путь в четыре поколения: первое поколение наживает, второе — приумножает, третье — транжирит, четвертое — возвращается на фабрику.',
#                            'Ничем так не завоюешь авторитета, как спокойствием.']
#
# Jason_Statham_quotes_en = ["I've come from nowhere, and I'm not shy to go back.",
#                            "You only get one shot in your life, and you might as well push yourself and try things.",
#                            "Revenge is a caustic thing. I say, breathe in, breathe deeply, let it go.",
#                            "How long you can continue to be good at something is how much you believe in yourself and how much hard work you do with the training.",
#                            "If you're going to do something, do it with style!",
#                            "Looking good and feeling good go hand in hand. If you have a healthy lifestyle, your diet and nutrition are set, and you're working out, you're going to feel good.",
#                            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
#                            "You have enemies? Good. That means you've stood up for something, sometime in your life.",
#                            "Men occasionally stumble over the truth, but most of them pick themselves up and hurry off as if nothing ever happened",
#                            "If you are going through hell, keep going.",
#                            "My tastes are simple: I am easily satisfied with the best.",
#                            "History will be kind to me for I intend to write it.",
#                            "Success is stumbling from failure to failure with no loss of enthusiasm.",
#                            "Tact is the ability to tell someone to go to hell in such a way that they look forward to the trip.",
#                            "Never, never, never give in!",
#                            "It is not enough that we do our best; sometimes we must do what is required.",
#                            "Nothing in life is so exhilarating as to be shot at without result.",
#                            "Kites rise highest against the wind, not with it.",
#                            "Never give in. Never give in. Never, never, never, never—in nothing, great or small, large or petty—never give in, except to convictions of honour and good sense. Never yield to force. Never yield to the apparently overwhelming might of the enemy.",
#                            "For myself I am an optimist - it does not seem to be much use to be anything else.",
#                            "Personally, I'm always ready to learn, although I do not always like being taught.",
#                            "A fanatic is one who can't change his mind and won't change the subject."]
#
#
# def motivate_users_with_Jason_Statham():
#     users = execute_database_command('SELECT id, language_code FROM users;')[0]
#
#     for user in users:
#         user_id = user[0]
#         language_code = user[1]
#
#         quote = random.choice(Jason_Statham_quotes_ru) + '\n\n*Джейсон Стэтхэм*' if language_code == 'ru' else \
#             random.choice(Jason_Statham_quotes_en) + '\n\n*Jason Statham*'
#
#         sticker = random.choice(Jason_Statham_sticker_pack)
#
#         try:
#             bot.send_message(user_id, quote, parse_mode='Markdown')
#             bot.send_sticker(user_id, sticker)
#         except Exception:
#             pass
