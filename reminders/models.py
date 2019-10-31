import abc
from utils.database import execute_database_command


class Reminder:
    def __init__(self, user_id, mid, datetime_native, datetime_utc, id=None):
        self.id = id
        self.user_id = user_id
        self.mid = mid
        self.datetime_native = datetime_native
        self.datetime_utc = datetime_utc

    @abc.abstractmethod
    def get(reminder_id):
        try:
            id, user_id, mid, datetime_native, datetime_utc = execute_database_command('SELECT * FROM reminders WHERE id=%s', (reminder_id, ))[0]
            return Reminder(user_id, mid, datetime_native, datetime_utc, id)
        except IndexError:
            return None

    def save(self):
        if Reminder.get(self.id):
            execute_database_command(
                f'UPDATE reminders SET '
                f'user_id = %s,'
                f'mid = %s,'
                f'''datetime_native = '{self.datetime_native}','''
                f'''datetime_utc = '{self.datetime_utc}','''
                f'WHERE id = %s',
                (self.user_id, self.mid, self.id)
            )
        else:
            reminder_id = execute_database_command(
                'INSERT INTO reminders (user_id, mid, datetime_native, datetime_utc) '
                f'''VALUES (%s, %s, '{self.datetime_native}', '{self.datetime_utc}') RETURNING id;''',
                (self.user_id, self.mid))[0][0]
            self.id = reminder_id

        return self

    def __str__(self):
        return f'{self.mid} (datetime: {self.datetime_native})'
