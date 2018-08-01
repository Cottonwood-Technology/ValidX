import sys
from time import time as timestamp
from datetime import date, time, datetime, timedelta

import pytest

from validateit import py, cy
from validateit import exc


if sys.version_info[0] < 3:
    str = unicode  # noqa


NoneType = type(None)
date_classes = [py.Date, cy.Date]
time_classes = [py.Time, cy.Time]
datetime_classes = [py.Datetime, cy.Datetime]


@pytest.mark.parametrize("class_", date_classes)
def test_date(class_):
    v = class_()
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today


@pytest.mark.parametrize("class_", date_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_date_nullable(class_, nullable):
    v = class_(nullable=nullable)
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == date
        assert info.value.actual == NoneType


@pytest.mark.parametrize("class_", date_classes)
@pytest.mark.parametrize("unixts", [None, False, True])
def test_date_unixts(class_, unixts):
    v = class_(unixts=unixts)
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today

    if unixts:
        assert v(timestamp()) == today
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(timestamp())
        assert info.value.expected == date
        assert info.value.actual == float


@pytest.mark.parametrize("class_", date_classes)
@pytest.mark.parametrize("format", [None, "%Y-%m-%d"])
def test_date_format(class_, format):
    v = class_(format=format)
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today

    if format:
        # Python 2.7 should handle both ``str`` and ``unicode``
        assert v("2018-07-03") == date(2018, 7, 3)
        assert v(u"2018-07-03") == date(2018, 7, 3)

        with pytest.raises(exc.DatetimeParseError) as info:
            v(u"03.07.2018")
        assert info.value.expected == format
        assert info.value.actual == u"03.07.2018"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(u"2018-07-03")
        assert info.value.expected == date
        assert info.value.actual == str


@pytest.mark.parametrize("class_", date_classes)
@pytest.mark.parametrize("min", [None, date(2018, 1, 1)])
@pytest.mark.parametrize("max", [None, date(2019, 1, 1)])
def test_date_min_max(class_, min, max):
    v = class_(min=min, max=max)
    assert v(date(2018, 7, 3)) == date(2018, 7, 3)

    if min is None:
        assert v(date(2017, 7, 3)) == date(2017, 7, 3)
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(date(2017, 7, 3))
        assert info.value.expected == min
        assert info.value.actual == date(2017, 7, 3)

    if max is None:
        assert v(date(2019, 7, 3)) == date(2019, 7, 3)
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(date(2019, 7, 3))
        assert info.value.expected == max
        assert info.value.actual == date(2019, 7, 3)


@pytest.mark.parametrize("class_", date_classes)
@pytest.mark.parametrize("relmin", [None, timedelta(days=1)])
@pytest.mark.parametrize("relmax", [None, timedelta(days=7)])
def test_date_relmin_relmax(class_, relmin, relmax):
    v = class_(relmin=relmin, relmax=relmax)
    today = date.today()
    assert v(today + timedelta(days=3)) == today + timedelta(days=3)

    if relmin is None:
        assert v(today) == today
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(today)
        assert info.value.expected == today + relmin
        assert info.value.actual == today

    if relmax is None:
        assert v(today + timedelta(days=9)) == today + timedelta(days=9)
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(today + timedelta(days=9))
        assert info.value.expected == today + relmax
        assert info.value.actual == today + timedelta(days=9)


# =============================================================================


@pytest.mark.parametrize("class_", time_classes)
def test_time(class_):
    v = class_()
    assert v(time(13, 35)) == time(13, 35)


@pytest.mark.parametrize("class_", time_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_time_nullable(class_, nullable):
    v = class_(nullable=nullable)
    assert v(time(13, 35)) == time(13, 35)

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == time
        assert info.value.actual == NoneType


@pytest.mark.parametrize("class_", time_classes)
@pytest.mark.parametrize("format", [None, "%H:%M"])
def test_time_format(class_, format):
    v = class_(format=format)
    assert v(time(13, 35)) == time(13, 35)

    if format:
        # Python 2.7 should handle both ``str`` and ``unicode``
        assert v("13:35") == time(13, 35)
        assert v(u"13:35") == time(13, 35)

        with pytest.raises(exc.DatetimeParseError) as info:
            v(u"13:35:00")
        assert info.value.expected == format
        assert info.value.actual == u"13:35:00"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(u"13:35")
        assert info.value.expected == time
        assert info.value.actual == str


@pytest.mark.parametrize("class_", time_classes)
@pytest.mark.parametrize("min", [None, time(8, 0)])
@pytest.mark.parametrize("max", [None, time(18, 0)])
def test_time_min_max(class_, min, max):
    v = class_(min=min, max=max)
    assert v(time(13, 35)) == time(13, 35)

    if min is None:
        assert v(time(3, 35)) == time(3, 35)
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(time(3, 35))
        assert info.value.expected == min
        assert info.value.actual == time(3, 35)

    if max is None:
        assert v(time(19, 35)) == time(19, 35)
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(time(19, 35))
        assert info.value.expected == max
        assert info.value.actual == time(19, 35)


# =============================================================================


@pytest.mark.parametrize("class_", datetime_classes)
def test_datetime(class_):
    v = class_()
    today = date.today()
    now = datetime.now()
    assert v(today) == datetime.combine(today, time())
    assert v(now) == now


@pytest.mark.parametrize("class_", datetime_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_datetime_nullable(class_, nullable):
    v = class_(nullable=nullable)
    today = date.today()
    now = datetime.now()
    assert v(today) == datetime.combine(today, time())
    assert v(now) == now

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == datetime
        assert info.value.actual == NoneType


@pytest.mark.parametrize("class_", datetime_classes)
@pytest.mark.parametrize("unixts", [None, False, True])
def test_datetime_unixts(class_, unixts):
    v = class_(unixts=unixts)
    today = date.today()
    now = datetime.now()
    assert v(today) == datetime.combine(today, time())
    assert v(now) == now

    if unixts:
        ts = timestamp()
        assert v(ts) == datetime.fromtimestamp(ts)
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(timestamp())
        assert info.value.expected == datetime
        assert info.value.actual == float


@pytest.mark.parametrize("class_", datetime_classes)
@pytest.mark.parametrize("format", [None, "%Y-%m-%dT%H:%M"])
def test_datetime_format(class_, format):
    v = class_(format=format)
    today = date.today()
    now = datetime.now()
    assert v(today) == datetime.combine(today, time())
    assert v(now) == now

    if format:
        # Python 2.7 should handle both ``str`` and ``unicode``
        assert v("2018-07-03T19:15") == datetime(2018, 7, 3, 19, 15)
        assert v(u"2018-07-03T19:15") == datetime(2018, 7, 3, 19, 15)

        with pytest.raises(exc.DatetimeParseError) as info:
            v(u"03.07.2018 19:15")
        assert info.value.expected == format
        assert info.value.actual == u"03.07.2018 19:15"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(u"2018-07-03T19:15")
        assert info.value.expected == datetime
        assert info.value.actual == str


@pytest.mark.parametrize("class_", datetime_classes)
@pytest.mark.parametrize("min", [None, datetime(2018, 1, 1)])
@pytest.mark.parametrize("max", [None, datetime(2019, 1, 1)])
def test_datetime_min_max(class_, min, max):
    v = class_(min=min, max=max)
    assert v(datetime(2018, 7, 3)) == datetime(2018, 7, 3)

    if min is None:
        assert v(datetime(2017, 7, 3)) == datetime(2017, 7, 3)
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(datetime(2017, 7, 3))
        assert info.value.expected == min
        assert info.value.actual == datetime(2017, 7, 3)

    if max is None:
        assert v(datetime(2019, 7, 3)) == datetime(2019, 7, 3)
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(datetime(2019, 7, 3))
        assert info.value.expected == max
        assert info.value.actual == datetime(2019, 7, 3)


@pytest.mark.parametrize("class_", datetime_classes)
@pytest.mark.parametrize("relmin", [None, timedelta(hours=1)])
@pytest.mark.parametrize("relmax", [None, timedelta(hours=7)])
def test_datetime_relmin_relmax(class_, relmin, relmax):
    v = class_(relmin=relmin, relmax=relmax)
    today = datetime.combine(date.today(), time())
    assert v(today + timedelta(hours=3)) == today + timedelta(hours=3)

    if relmin is None:
        assert v(today) == today
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(today)
        assert info.value.expected == today + relmin
        assert info.value.actual == today

    if relmax is None:
        assert v(today + timedelta(hours=9)) == today + timedelta(hours=9)
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(today + timedelta(hours=9))
        assert info.value.expected == today + relmax
        assert info.value.actual == today + timedelta(hours=9)
