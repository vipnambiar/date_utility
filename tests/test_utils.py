from datetime import datetime
from utils.date_util import get_next_business_day_time, add_days, add_hours
import pytest
from pytz import timezone


def test_get_next_business_day_time():
    central = timezone("US/Central")
    current_time = central.localize(datetime(2017, 8, 14, 18, 45, 0))
    st_time_tuple = (9, 30, 0)
    next_business_st_time = get_next_business_day_time(current_time, st_time_tuple)
    dt = datetime(2017, 8, 16, 9, 30, 0)
    nt = central.localize(dt)
    assert next_business_st_time == nt


def test_add_days():
    central = timezone("US/Central")
    current_time = central.localize(datetime(2017, 8, 11, 18, 45, 0))
    days = 10
    new_dt = add_days(current_time, days, business_day=True)
    dt = central.localize(datetime(2017, 8, 28, 18, 45, 0))
    assert new_dt == dt


def test_add_business_hours():
    central = timezone("US/Central")
    dt = datetime(2017, 8, 25, 17, 30, 0)
    result_dt = add_hours(current_date=central.localize(dt),
                          hours=24.75,
                          business_day=True,
                          business_hour=True,
                          start_time=(10, 0, 0),
                          end_time=(18, 0, 0)
                          )
    new_dt = central.localize(datetime(2017, 8, 31, 10, 15, 0))
    assert result_dt == new_dt


def test_add_business_days():
    central = timezone("US/Central")
    dt = datetime(2017, 8, 25, 17, 30, 0)
    result_dt = add_hours(current_date=central.localize(dt),
                          hours=24.75,
                          business_day=True,
                          business_hour=False,
                          start_time=(10, 0, 0),
                          end_time=(18, 0, 0)
                          )
    new_dt = central.localize(datetime(2017, 8, 28, 18, 15, 0))
    assert result_dt == new_dt


def test_add_hours():
    central = timezone("US/Central")
    dt = datetime(2017, 8, 25, 17, 30, 0)
    result_dt = add_hours(current_date=central.localize(dt),
                          hours=24.75,
                          business_day=False,
                          business_hour=False,
                          start_time=(10, 0, 0),
                          end_time=(18, 0, 0)
                          )
    new_dt = central.localize(datetime(2017, 8, 26, 18, 15, 0))
    assert result_dt == new_dt


if __name__ == '__main__':
    pytest.main()
