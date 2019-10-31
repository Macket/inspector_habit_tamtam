import datetime
import pytz
from users.utils import get_native_datetime


def get_datetimes(day_of_week, time, timezone):
    day = datetime.datetime.now(tz=pytz.timezone(timezone)).date()
    if isinstance(day_of_week, int):
        if day_of_week > day.weekday():
            day = day + datetime.timedelta(day_of_week - day.weekday())
        else:
            day = day + datetime.timedelta(7 - day.weekday() + day_of_week)
    elif day_of_week == 'tomorrow':
        day = (datetime.datetime.now(tz=pytz.timezone(timezone)) + datetime.timedelta(1)).date()

    datetime_native = get_native_datetime(str(day), time, timezone)
    datetime_utc = datetime_native.astimezone(pytz.utc)

    return datetime_native, datetime_utc
