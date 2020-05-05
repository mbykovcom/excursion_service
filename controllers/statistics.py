from datetime import datetime, timedelta
from math import ceil
from typing import Tuple

from fastapi import HTTPException
from starlette import status

from database import db
from models.listening import Listening
from models.other import Statistics

CALENDAR = {1: (datetime(2019, 1, 1, 0, 0), datetime(2019, 1, 31, 23, 59, 59, 999999)),
            2: [datetime(2019, 2, 1, 0, 0), datetime(2019, 2, 28, 23, 59, 59, 999999)],
            3: (datetime(2019, 3, 1, 0, 0), datetime(2019, 3, 31, 23, 59, 59, 999999)),
            4: (datetime(2019, 4, 1, 0, 0), datetime(2019, 4, 30, 23, 59, 59, 999999)),
            5: (datetime(2019, 5, 1, 0, 0), datetime(2019, 5, 31, 23, 59, 59, 999999)),
            6: (datetime(2019, 6, 1, 0, 0), datetime(2019, 6, 30, 23, 59, 59, 999999)),
            7: (datetime(2019, 7, 1, 0, 0), datetime(2019, 7, 31, 23, 59, 59, 999999)),
            8: (datetime(2019, 8, 1, 0, 0), datetime(2019, 8, 31, 23, 59, 59, 999999)),
            9: (datetime(2019, 9, 1, 0, 0), datetime(2019, 9, 30, 23, 59, 59, 999999)),
            10: (datetime(2019, 10, 1, 0, 0), datetime(2019, 10, 31, 23, 59, 59, 999999)),
            11: (datetime(2019, 11, 1, 0, 0), datetime(2019, 11, 30, 23, 59, 59, 999999)),
            12: (datetime(2019, 12, 1, 0, 0), datetime(2019, 12, 31, 23, 59, 59, 999999))}


def specify_period(start: datetime, end: datetime) -> Tuple[datetime, datetime]:
    now = datetime.now()
    if start is None and end is None:
        day = now.isoweekday()
        start = now - timedelta(days=day - 1)
        end = now + timedelta(days=7 - day)
    if end is None:
        end = now
    if start is None:
        day = now.isoweekday()
        start = now - timedelta(days=day - 1)
    return start, end


def generating_segments(period: Tuple[datetime, datetime]) -> Tuple[str, dict]:
    delta = period[1] - period[0]
    if delta < timedelta(minutes=15):
        return None

    elif delta < timedelta(minutes=61):
        value = 'minutes'
        n = round(delta / timedelta(minutes=15), 3)
        inc = timedelta(minutes=15)
        start = period[0]
        end = period[0] + inc

    elif delta < timedelta(minutes=60 * 24 + 1):
        value = 'hours'
        n = round(delta / timedelta(minutes=60), 3)
        inc = timedelta(hours=1)
        start = period[0]
        end = period[0] + inc

    elif delta < timedelta(days=8):
        value = 'days'
        n = float(delta.days)
        inc = timedelta(days=1)
        start = datetime(year=period[0].year, month=period[0].month, day=period[0].day)
        end = datetime(year=period[0].year, month=period[0].month, day=period[0].day) + timedelta(days=1) \
              - timedelta(microseconds=1)

    elif delta < timedelta(days=36):
        value = 'weeks'
        n = ceil(round(delta / timedelta(days=7), 3))
        inc = timedelta(days=7)
        start = datetime(year=period[0].year, month=period[0].month, day=period[0].day)
        end = datetime(year=period[0].year, month=period[0].month, day=period[0].day) + timedelta(days=7) \
              - timedelta(microseconds=1)

    elif delta < timedelta(days=367):
        if period[0].day != 1:
            return None
        value = 'months'
        m = period[0].month
        if m > 2:
            y = period[1].year
        else:
            y = period[0].year
        if not (y % 4 != 0 or (y % 100 == 0 and y % 400 != 0)):
            CALENDAR[2][1] = datetime(y, 2, 29, 23, 59, 59, 999999)
        dict_segment = {}
        y = period[0].year
        flag = True
        for i in range(0, 12):
            n = m + i
            if n > 12:
                n = m + i - 12
                if flag:
                    y += 1
                    flag = False
            dict_segment[i + 1] = [datetime(y, month=CALENDAR[n][0].month, day=CALENDAR[n][0].day,
                                            hour=CALENDAR[n][0].hour, minute=CALENDAR[n][0].minute,
                                            second=CALENDAR[n][0].second, microsecond=CALENDAR[n][0].microsecond),
                                   datetime(y, month=CALENDAR[n][1].month, day=CALENDAR[n][1].day,
                                            hour=CALENDAR[n][1].hour, minute=CALENDAR[n][1].minute,
                                            second=CALENDAR[n][1].second, microsecond=CALENDAR[n][1].microsecond)]
        return value, dict_segment
    else:
        return None

    dict_segment = {}
    i = 1
    delta_inc = timedelta(0)
    while n > 0:
        if n < 1:
            dict_segment[i] = [start + delta_inc, period[1]]
        else:
            dict_segment[i] = [start + delta_inc, end + delta_inc]
        delta_inc += inc
        n -= 1
        i += 1
    return value, dict_segment


def get_statistics_users(period: Tuple[datetime, datetime]) -> Statistics:
    segments = generating_segments(period)
    if segments is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid time interval')
    count = [0 for i in range(0, len(segments[1]))]
    for i in range(len(segments[1])):
        count[i] = db.get_user_statistics(segments[1][i+1][0], segments[1][i+1][1])
    data = {i+1: c for i, c in enumerate(count)}
    return Statistics(type=segments[0], data=data)


def get_statistics_excursions(period: Tuple[datetime, datetime]) -> Statistics:
    segments = generating_segments(period)
    if segments is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid time interval')
    count = [0 for i in range(0, len(segments[1]))]
    for i in range(len(segments[1])):
        count[i] = db.get_excursion_statistics(segments[1][i + 1][0], segments[1][i + 1][1])
    data = {i + 1: c for i, c in enumerate(count)}
    return Statistics(type=segments[0], data=data)


def get_statistics_listening(period: Tuple[datetime, datetime]) -> Statistics:
    segments = generating_segments(period)
    if segments is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid time interval')
    count = [0 for i in range(0, len(segments[1]))]
    for i in range(len(segments[1])):
        count[i] = db.get_listening_statistics(segments[1][i + 1][0], segments[1][i + 1][1])
    data = {i + 1: c for i, c in enumerate(count)}
    return Statistics(type=segments[0], data=data)


def get_statistics_sales(period: Tuple[datetime, datetime]) -> Statistics:
    segments = generating_segments(period)
    if segments is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid time interval')
    sum = [0. for i in range(0, len(segments[1]))]
    for i in range(len(segments[1])):
        excursions = db.get_sales_statistics(segments[1][i + 1][0], segments[1][i + 1][1])
        list_excursion = db.get_items_by_list_id('excursions', [excursion['_id'] for excursion in excursions])
        for excursion_db, exc in zip(list_excursion, excursions):
            sum[i] += excursion_db.price * exc['count']
    data = {i + 1: s for i, s in enumerate(sum)}
    return Statistics(type=segments[0], data=data)


def add_listening(listen: Listening) -> Listening:
    if listen._id is None:
        listen._id = db.get_last_id('listening').last_id
    return db.add(listen)