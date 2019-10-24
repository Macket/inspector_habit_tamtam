import abc
import ast
from utils.database import execute_database_command


class Plan:
    def __init__(self, user_id, plan_array, status_array, date, id=None):
        self.id = id
        self.user_id = user_id
        self.plan_array = plan_array
        self.status_array = status_array
        self.date = date

    @abc.abstractmethod
    def get(plan_id):
        try:
            id, user_id, plan_array, status_array, date = execute_database_command('SELECT * FROM plans WHERE id=%s', (plan_id, ))[0]
            plan_array = ast.literal_eval(plan_array.replace('{', '[').replace('}', ']'))
            status_array = ast.literal_eval(status_array.replace('{', '[').replace('}', ']'))
            return Plan(user_id, plan_array, status_array, date, id)
        except IndexError:
            return None

    def save(self):
        plan_array = [*self.plan_array]
        plan_array = str(list(map(str, plan_array)))
        plan_array = plan_array.replace('[', '{').replace(']', '}').replace('\'', '\"')

        status_array = [*self.status_array]
        status_array = str(list(map(str, status_array)))
        status_array = status_array.replace('[', '{').replace(']', '}').replace('\'', '\"')

        if Plan.get(self.id):
            execute_database_command(
                'UPDATE plans SET user_id = %s, plan_array = %s, status_array = %s, date = %s WHERE id = %s',
                (self.user_id, plan_array, status_array, self.date, self.id)
            )
        else:
            plan_id = execute_database_command(
                'INSERT INTO plans (user_id, plan_array, status_array, date) VALUES (%s, %s, %s, %s) RETURNING id;',
                (self.user_id, plan_array, status_array, self.date)
            )[0][0]

            self.id = plan_id

        return self

    # def get_remaining_checks(self):
    #     return execute_database_command(
    #         'SELECT id FROM checks WHERE habit_id = %s AND (status = %s OR status = %s)',
    #         (self.id, CheckStatus.PENDING.value, CheckStatus.CHECKING.value)
    #     )

    def __str__(self):
        return f'{self.plan_array} (date: {self.date})'
