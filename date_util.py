import calendar as cl
from datetime import date, datetime, timedelta
from pytz import tzinfo


HOLIDAYS = [
    (26, 1),
    (1, 5),
    (15, 8),
    (2, 10),
    (1, 11)
]

WEEKEND = (cl.SATURDAY, cl.SUNDAY)


def is_business_day(date_obj):
    weekday = date_obj.weekday()
    day = date_obj.day
    mth = date_obj.month
    return weekday not in WEEKEND and (day, mth) not in HOLIDAYS


def increment_day(current_date,
                  business_day=False):
    delta = timedelta(days=1)
    if not business_day:
        return current_date + delta
    else:
        next_day = current_date + delta
        if not is_business_day(next_day):
            return increment_day(next_day,
                                 business_day=business_day)
        else:
            return next_day


def get_next_business_day_time(current_date, time_tuple):
    next_business_date = increment_day(current_date, business_day=True)
    return datetime(next_business_date.year,
                    next_business_date.month,
                    next_business_date.day,
                    time_tuple[0],
                    time_tuple[1],
                    time_tuple[2],
                    tzinfo=next_business_date.tzinfo()
                    )


"""
    else:
        st_time_seconds = start_time[0]*60*60 + start_time[1]*60 + start_time[2]
        end_time_seconds = end_time[0]*60*60 + end_time[1]*60 + end_time[2]
        delta_seconds = end_time_seconds - st_time_seconds
"""
