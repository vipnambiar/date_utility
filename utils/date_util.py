import calendar as cl
from datetime import datetime, timedelta
from pytz import timezone


HOLIDAYS = [
    (26, 1),
    (1, 5),
    (15, 8),
    (2, 10),
    (1, 11)
]

WEEKEND = (cl.SATURDAY, cl.SUNDAY)


def is_business_day(date_obj):
    """Returns True if given date obj is not a weekend nor a holiday
    """
    weekday = date_obj.weekday()
    day = date_obj.day
    mth = date_obj.month
    return weekday not in WEEKEND and (day, mth) not in HOLIDAYS


def increment_day(current_date, business_day=False):
    """
    Increment a day to the given date obj.
    If business_day flag is True, excludes weekends and holidays for calculation
    """
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


def get_next_business_day_time(current_date, time_tuple=None):
    """
    Returns next business day after the current date.
    Excludes weekends and holidays for calculation.
    If time_tuple is provided, corresponding time of the next business day is returned
    else returns time corresponding to current_date.
    """
    next_business_date = increment_day(current_date, business_day=True)
    if time_tuple:
        return datetime(next_business_date.year,
                        next_business_date.month,
                        next_business_date.day,
                        time_tuple[0],
                        time_tuple[1],
                        time_tuple[2],
                        tzinfo=next_business_date.tzinfo
                        )
    else:
        return next_business_date


def add_days(current_date, days=1, business_day=False):
    """
    @curent_date: timezone aware datetime object
    @days: number of days to be added - Integer
    @business_day: Consider only business days - Boolean

    returns: datetime time object after adding the specified days to current_date
    """
    days_to_add = days
    next_date = current_date
    while days_to_add:
        next_date = increment_day(next_date, business_day)
        days_to_add -= 1
    return next_date


def add_hours(current_date,
              hours=1,
              business_day=False,
              business_hour=False,
              start_time=None,
              end_time=None):
    """
    @current_date: timezone aware datetime object
    @hours: number of hours to be added - float
    @business_day: Consider only business days - Boolean
    @business_hour: Consider only business hour - Boolean
    @start_time: (hour, minute, seconds) - 3 integer Tuple

    Returns date and time after adding the specified hours.
    If business_day flag is True, excludes weekends and holidays for calculation.
    If business_hour flag is True, considers only business hours between start_time and end_time for calculation
    """
    time_to_add = timedelta(hours=hours)
    if business_day and business_hour and (not start_time or not end_time):
        raise ValueError("For business hours, both start time and end time are mandatory!")
    elif business_day and business_hour:
        start_of_day = datetime(current_date.year,
                                current_date.month,
                                current_date.day,
                                start_time[0],
                                start_time[1],
                                start_time[2],
                                tzinfo=current_date.tzinfo
                                )
        end_of_day = datetime(current_date.year,
                              current_date.month,
                              current_date.day,
                              end_time[0],
                              end_time[1],
                              end_time[2],
                              tzinfo=current_date.tzinfo
                              )
        total_business_hours = end_of_day - start_of_day
        if current_date >= start_of_day and current_date <= end_of_day:
            time_left = end_of_day - current_date
        elif current_date < start_of_day:
            time_left = end_of_day - start_of_day
            current_date = start_of_day
        else:
            time_left = end_of_day - end_of_day
        while time_to_add:
            if time_to_add < time_left:
                current_date = current_date + time_to_add
                break
            else:
                next_date = get_next_business_day_time(current_date, start_time)
                time_to_add = time_to_add - time_left
                if time_to_add < total_business_hours:
                    current_date = next_date + time_to_add
                    break
                else:
                    time_left = total_business_hours
                    current_date = next_date
                    continue
        return current_date
    elif business_day:
        end_of_day = datetime(current_date.year,
                              current_date.month,
                              current_date.day,
                              0,
                              0,
                              0,
                              tzinfo=current_date.tzinfo
                              ) + timedelta(hours=24)
        time_left = end_of_day - current_date
        while time_to_add:
            if time_to_add < time_left:
                current_date = current_date + time_to_add
                break
            else:
                next_date = get_next_business_day_time(current_date, (0, 0, 0))
                time_to_add = time_to_add - time_left
                if time_to_add < timedelta(days=1):
                    current_date = next_date + time_to_add
                    break
                else:
                    time_left = timedelta(days=1)
                    current_date = next_date
                    continue
        return current_date
    else:
        return current_date + timedelta(hours=hours)


if __name__ == '__main__':
    central = timezone("US/Central")
    dt = datetime(2017, 8, 25, 18, 30, 0)
    print add_hours(current_date=central.localize(dt),
                    hours=26.5,
                    business_day=True,
                    business_hour=False,
                    start_time=(10, 0, 0),
                    end_time=(18, 0, 0)
                    )
