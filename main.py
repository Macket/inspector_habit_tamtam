# -*- coding: UTF-8 -*-
import time
import datetime
from timeloop import Timeloop
from bot import bot
from utils.database import init_database
from checks.checks import check_users, rate_users
from reminders.crons import remind_users

tl = Timeloop()
last_check_utc = datetime.datetime.strptime(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")  # TODO поправить
last_remind_utc = datetime.datetime.strptime(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")  # TODO поправить


@tl.job(interval=datetime.timedelta(minutes=1))
def check_users_job():
    global last_check_utc
    last_check_utc = check_users(last_check_utc)


@tl.job(interval=datetime.timedelta(minutes=1))
def remind_users_job():
    global last_remind_utc
    last_remind_utc = remind_users(last_remind_utc)


# @tl.job(interval=datetime.timedelta(hours=20))
# def motivate_users_with_Jason_Statham_job():
#     motivate_users_with_Jason_Statham()


@tl.job(interval=datetime.timedelta(days=3))
def rate_users_job():
    rate_users()


init_database()

tl.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        tl.stop()
        print('stop')
    break

bot.polling_sleep_time = 1
while True:
    try:
        bot.polling()
    except:
        time.sleep(10)
