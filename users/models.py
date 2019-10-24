import abc
import ast
import datetime
import pytz
from plans.models import Plan
from utils.database import execute_database_command


class User:
    def __init__(self, tamtam_id, chat_id, username=None, first_name=None, last_name=None, timezone=None, language_code=None, is_active=True, referrer=None, score=0):
        self.id = tamtam_id
        self.chat_id = chat_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.timezone = timezone
        self.language_code = language_code
        self.is_active = is_active
        self.referrer = referrer
        self.score = score

    @abc.abstractmethod
    def get(tamtam_id):
        try:
            id, chat_id, username, first_name, last_name, timezone, language_code, is_active, referrer, score = execute_database_command('SELECT * FROM users WHERE id=%s', (tamtam_id, ))[0]
            return User(id, chat_id, username, first_name, last_name, timezone, language_code, is_active, referrer, score)
        except IndexError:
            return None

    def save(self):
        if User.get(self.id):
            execute_database_command(
                'UPDATE users SET chat_id = %s, username = %s, first_name = %s, last_name = %s, timezone = %s, language_code = %s, is_active = %s, referrer=%s, score=%s WHERE id = %s',
                (self.chat_id, self.username, self.first_name, self.last_name, self.timezone, self.language_code, self.is_active, self.referrer, self.score, self.id)
            )
        else:
            execute_database_command(
                'INSERT INTO users (id, chat_id, username, first_name, last_name, timezone, language_code, is_active, referrer, score)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (self.id, self.chat_id, self.username, self.first_name, self.last_name, self.timezone, self.language_code, self.is_active, self.referrer, self.score)
            )

    @property
    def today_plan(self):
        today = datetime.datetime.now(tz=pytz.timezone(self.timezone)).date()
        try:
            id, user_id, plan_array, status_array, date = \
                execute_database_command('SELECT * FROM plans WHERE user_id=%s AND date=%s', (self.id, today))[0]
            plan_array = ast.literal_eval(plan_array.replace('{', '[').replace('}', ']'))
            status_array = ast.literal_eval(status_array.replace('{', '[').replace('}', ']'))
            return Plan(user_id, plan_array, status_array, date, id)
        except:
            return None

    @property
    def tomorrow_plan(self):
        tomorrow = (datetime.datetime.now(tz=pytz.timezone(self.timezone)) +
                    datetime.timedelta(1)).date()
        try:
            id, user_id, plan_array, status_array, date = \
                execute_database_command('SELECT * FROM plans WHERE user_id=%s AND date=%s', (self.id, tomorrow))[0]
            plan_array = ast.literal_eval(plan_array.replace('{', '[').replace('}', ']'))
            status_array = ast.literal_eval(status_array.replace('{', '[').replace('}', ']'))
            return Plan(user_id, plan_array, status_array, date, id)
        except:
            return None

    def __str__(self):
        return f'{self.username if self.username else "No name"} (id: {self.id})'
