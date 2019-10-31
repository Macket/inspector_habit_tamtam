import pytz

from openapi_client import NewMessageLink, MessageLinkType, NewMessageBody
import speech_recognition as sr
import subprocess
import urllib
import re
from users.models import User
from .utils import get_datetimes
from .models import Reminder
import datetime

days_dict = {
    'понедельник': 0,
    'вторник': 1,
    'среда': 2,
    'четверг': 3,
    'пятница': 4,
    'суббота': 5,
    'воскресенье': 6,
    'сегодня': 'today',
    'завтра': 'tomorrow',
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6,
    'today': 'today',
    'tomorrow': 'tomorrow',
}


def handle_audio(bot, update):
    user = User.get(update.user_id)
    url = update.message.body.attachments[0].payload.url
    urllib.request.urlretrieve(url, 'temp.mp3')
    subprocess.call(['ffmpeg', '-y', '-i', 'temp.mp3', 'temp.wav'])

    r = sr.Recognizer()
    with sr.AudioFile('temp.wav') as source:
        audio = r.record(source)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        recognized_text = r.recognize_google(audio, language=user.language_code).lower()
    except sr.UnknownValueError:
        bot.send_message(update.user_id,
                         'Не понял тебя, попробуй ещё раз' if user.language_code == 'ru' else
                         "Don't understand you, try again")
        return
    except sr.RequestError:
        bot.send_message(update.user_id,
                         'Что-то пошло не так, попробуй ещё раз' if user.language_code == 'ru' else
                         "Something went wrong, try again")
        return

    day_of_week = None
    for day in days_dict.keys():
        if day in recognized_text:
            day_of_week = days_dict[day]
            break

    time = None
    if re.findall(r'\d{1,2}:\d{2} p.m.', recognized_text):
        time = re.findall(r'\d{1,2}:\d{2}', recognized_text)[0]
        hours = int(time[:time.index(':')])
        if hours < 12:
            hours += 12
            time = str(hours) + time[time.index(':'):]
    elif re.findall(r'\d{1,2} p.m.', recognized_text):
        time = re.findall(r'\d{1,2} p.m.', recognized_text)[0]
        hours = int(time[:-5])
        if hours < 12:
            hours += 12
            time = str(hours) + ':00'
    elif re.findall(r'\d{1,2}:\d{2} a.m.', recognized_text):
        time = re.findall(r'\d{1,2}:\d{2} a.m.', recognized_text)
    elif re.findall(r'\d{1,2} a.m.', recognized_text):
        time = re.findall(r'\d{1,2} a.m.', recognized_text)[0]
        time = time[:-5] + ':00'
    elif re.findall(r'\d{1,2}:\d{2}', recognized_text):
        time = re.findall(r'\d{1,2}:\d{2}', recognized_text)[0]

    if day_of_week and time:
        datetime_native, datetime_utc = get_datetimes(day_of_week, time, user.timezone)

        if datetime_utc.replace(tzinfo=None) > datetime.datetime.utcnow():
            Reminder(update.user_id, update.message.body.mid, datetime_native, datetime_utc).save()
            ru_text = f'Хорошо, я напомню тебе об этом {datetime_native.strftime("%d.%m.%Y")} в {time}'
            en_text = f'Ok, I will remind you about it on {datetime_native.strftime("%d.%m.%Y")} at {time}'
            text = ru_text if user.language_code == 'ru' else en_text
            bot.reply_message(update.user_id, update.message.body.mid, text)
        else:
            ru_text = f'Я не умею возвращаться в прошлое🙂'
            en_text = f"I don't know how to return to the past🙂"
            text = ru_text if user.language_code == 'ru' else en_text
            bot.send_message(update.user_id, text)
    else:
        text = 'Ты не сказал ' if user.language_code == 'ru' else 'You did not say '
        if not day_of_week and not time:
            text += 'день и время' if user.language_code == 'ru' else 'a day and time'
        elif not day_of_week:
            text += 'день' if user.language_code == 'ru' else 'a day'
        else:
            text += 'время' if user.language_code == 'ru' else 'time'

        bot.send_message(update.user_id, text)
