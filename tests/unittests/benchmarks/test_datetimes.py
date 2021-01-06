from time import time as timestamp
from datetime import date, time, datetime, timedelta

import pytest


@pytest.mark.benchmark(group="Date")
def test_date(module, benchmark):
    v = module.Date()
    today = date.today()
    assert benchmark(v, today) == today


@pytest.mark.benchmark(group="Date")
def test_date_coerce_datetime(module, benchmark):
    v = module.Date()
    today = date.today()
    now = datetime.now()
    assert benchmark(v, now) == today


@pytest.mark.benchmark(group="Date")
def test_date_nullable(module, benchmark):
    v = module.Date(nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Date")
def test_date_unixts(module, benchmark):
    v = module.Date(unixts=True)
    today = date.today()
    ts = timestamp()
    assert benchmark(v, ts) == today


@pytest.mark.benchmark(group="Date")
def test_date_format(module, benchmark):
    v = module.Date(format="%Y-%m-%d")
    assert benchmark(v, "2018-07-03") == date(2018, 7, 3)


@pytest.mark.benchmark(group="Date")
def test_date_min_max(module, benchmark):
    v = module.Date(min=date(2018, 1, 1), max=date(2019, 1, 1))
    assert benchmark(v, date(2018, 7, 3)) == date(2018, 7, 3)


@pytest.mark.benchmark(group="Date")
def test_date_relmin_relmax(module, benchmark):
    v = module.Date(relmin=timedelta(days=1), relmax=timedelta(days=7))
    today = date.today()
    assert benchmark(v, today + timedelta(days=3)) == today + timedelta(days=3)


# =============================================================================


@pytest.mark.benchmark(group="Time")
def test_time(module, benchmark):
    v = module.Time()
    assert benchmark(v, time(13, 35)) == time(13, 35)


@pytest.mark.benchmark(group="Time")
def test_time_nullable(module, benchmark):
    v = module.Time(nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Time")
def test_time_format(module, benchmark):
    v = module.Time(format="%H:%M")
    assert benchmark(v, "13:35") == time(13, 35)


@pytest.mark.benchmark(group="Time")
def test_time_min_max(module, benchmark):
    v = module.Time(min=time(8, 0), max=time(18, 0))
    assert benchmark(v, time(13, 35)) == time(13, 35)


# =============================================================================


@pytest.mark.benchmark(group="Datetime")
def test_datetime(module, benchmark):
    v = module.Datetime()
    now = datetime.now()
    assert benchmark(v, now) == now


@pytest.mark.benchmark(group="Datetime")
def test_datetime_coerce_date(module, benchmark):
    v = module.Datetime()
    today = date.today()
    assert benchmark(v, today) == datetime.combine(today, time())


@pytest.mark.benchmark(group="Datetime")
def test_datetime_nullable(module, benchmark):
    v = module.Datetime(nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Datetime")
def test_datetime_unixts(module, benchmark):
    v = module.Datetime(unixts=True)
    ts = timestamp()
    assert benchmark(v, ts) == datetime.fromtimestamp(ts)


@pytest.mark.benchmark(group="Datetime")
def test_datetime_format(module, benchmark):
    v = module.Datetime(format="%Y-%m-%dT%H:%M")
    assert benchmark(v, "2018-07-03T19:15") == datetime(2018, 7, 3, 19, 15)


@pytest.mark.benchmark(group="Datetime")
def test_datetime_min_max(module, benchmark):
    v = module.Datetime(min=datetime(2018, 1, 1), max=datetime(2019, 1, 1))
    assert benchmark(v, datetime(2018, 7, 3)) == datetime(2018, 7, 3)


@pytest.mark.benchmark(group="Datetime")
def test_datetime_relmin_relmax(module, benchmark):
    v = module.Datetime(relmin=timedelta(hours=1), relmax=timedelta(hours=7))
    now = datetime.now()
    assert benchmark(v, now + timedelta(hours=3)) == now + timedelta(hours=3)
