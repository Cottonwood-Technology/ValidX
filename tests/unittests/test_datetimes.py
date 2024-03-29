import pickle
from time import time as timestamp
from datetime import date, time, datetime, timedelta

import pytest
from dateutil.parser import isoparse as _isoparse, parse as dtparse
from pytz import UTC, timezone

from validx import exc
from validx import platform


def isoparse(*args, **kw):
    """Pickleable version of date/time parser"""
    return _isoparse(*args, **kw)


EST = timezone("US/Eastern")
NoneType = type(None)


def test_date(module):
    v = module.Date()
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v


@pytest.mark.parametrize("nullable", [None, False, True])
def test_date_nullable(module, nullable):
    v = module.Date(nullable=nullable)
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == date
        assert info.value.actual == NoneType


@pytest.mark.parametrize("unixts", [None, False, True])
def test_date_unixts(module, unixts):
    v = module.Date(unixts=unixts)
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if unixts:
        assert v(timestamp()) == today

        # Should handle ``ValueError`` on 64-bit machine
        with pytest.raises(exc.MaxValueError) as info:
            v(1 << 50)
        assert info.value.expected == platform.MAX_TIMESTAMP
        assert info.value.actual == 1 << 50

        with pytest.raises(exc.MinValueError) as info:
            v(-1 << 50)
        assert info.value.expected == platform.MIN_TIMESTAMP
        assert info.value.actual == -1 << 50

        # Should handle ``OSError`` on 64-bit machine
        with pytest.raises(exc.MaxValueError) as info:
            v(1 << 60)
        assert info.value.expected == platform.MAX_TIMESTAMP
        assert info.value.actual == 1 << 60

        with pytest.raises(exc.MinValueError) as info:
            v(-1 << 60)
        assert info.value.expected == platform.MIN_TIMESTAMP
        assert info.value.actual == -1 << 60

        # Should handle ``OverflowError`` on 64-bit machine
        with pytest.raises(exc.MaxValueError) as info:
            v(1 << 70)
        assert info.value.expected == platform.MAX_TIMESTAMP
        assert info.value.actual == 1 << 70

        with pytest.raises(exc.MinValueError) as info:
            v(-1 << 70)
        assert info.value.expected == platform.MIN_TIMESTAMP
        assert info.value.actual == -1 << 70

        with pytest.raises(exc.InvalidTypeError) as info:
            v(True)
        assert info.value.expected == date
        assert info.value.actual == bool
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(timestamp())
        assert info.value.expected == date
        assert info.value.actual == float


@pytest.mark.parametrize("format", [None, "%Y-%m-%d"])
def test_date_format(module, format):
    v = module.Date(format=format)
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if format:
        assert v("2018-07-03") == date(2018, 7, 3)

        with pytest.raises(exc.DatetimeParseError) as info:
            v("03.07.2018")
        assert info.value.expected == format
        assert info.value.actual == "03.07.2018"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("2018-07-03")
        assert info.value.expected == date
        assert info.value.actual == str


@pytest.mark.parametrize("parser", [None, isoparse])
def test_date_parser(module, parser):
    v = module.Date(parser=parser)
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if parser:
        assert v("2018-07-03") == date(2018, 7, 3)

        with pytest.raises(exc.DatetimeParseError) as info:
            v("03.07.2018")
        assert info.value.expected == parser
        assert info.value.actual == "03.07.2018"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("2018-07-03")
        assert info.value.expected == date
        assert info.value.actual == str


@pytest.mark.parametrize("min", [None, date(2018, 1, 1)])
@pytest.mark.parametrize("max", [None, date(2019, 1, 1)])
def test_date_min_max(module, min, max):
    v = module.Date(min=min, max=max)
    assert v(date(2018, 7, 3)) == date(2018, 7, 3)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

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


@pytest.mark.parametrize("relmin", [None, timedelta(days=1)])
@pytest.mark.parametrize("relmax", [None, timedelta(days=7)])
def test_date_relmin_relmax(module, relmin, relmax):
    v = module.Date(relmin=relmin, relmax=relmax)
    today = date.today()
    assert v(today + timedelta(days=3)) == today + timedelta(days=3)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

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


@pytest.mark.parametrize("tz", [None, EST])
def test_date_tz(module, tz):
    v = module.Date(unixts=True, parser=isoparse, tz=tz)
    today = date.today()
    now = datetime.now()
    assert v(today) == today
    assert v(now) == today
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if tz is not None:
        assert v(datetime(2018, 12, 5, tzinfo=UTC)) == date(2018, 12, 4)
        assert v("2018-12-05T00:00:00Z") == date(2018, 12, 4)
        assert v(1543968000) == date(2018, 12, 4)
    else:
        assert v(datetime(2018, 12, 5, tzinfo=UTC)) == date(2018, 12, 5)
        assert v("2018-12-05T00:00:00Z") == date(2018, 12, 5)
        # Actual value below depends on system locale
        assert v(1543968000) == date.fromtimestamp(1543968000)


@pytest.mark.parametrize("tz", [timezone("Etc/GMT-14"), timezone("Etc/GMT+12")])
def test_date_relmin_relmax_with_tz(module, tz):
    v = module.Date(relmin=-timedelta(days=1), relmax=timedelta(days=1), tz=tz)
    today = datetime.now(UTC).astimezone(tz).date()
    assert v(today - timedelta(days=1)) == today - timedelta(days=1)
    assert v(today + timedelta(days=1)) == today + timedelta(days=1)


# =============================================================================


def test_time(module):
    v = module.Time()
    assert v(time(13, 35)) == time(13, 35)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v


@pytest.mark.parametrize("nullable", [None, False, True])
def test_time_nullable(module, nullable):
    v = module.Time(nullable=nullable)
    assert v(time(13, 35)) == time(13, 35)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == time
        assert info.value.actual == NoneType


@pytest.mark.parametrize("format", [None, "%H:%M"])
def test_time_format(module, format):
    v = module.Time(format=format)
    assert v(time(13, 35)) == time(13, 35)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if format:
        assert v("13:35") == time(13, 35)

        with pytest.raises(exc.DatetimeParseError) as info:
            v("13:35:00")
        assert info.value.expected == format
        assert info.value.actual == "13:35:00"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("13:35")
        assert info.value.expected == time
        assert info.value.actual == str


@pytest.mark.parametrize("parser", [None, dtparse])
def test_time_parse(module, parser):
    v = module.Time(parser=parser)
    assert v(time(13, 35)) == time(13, 35)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if parser:
        assert v("13:35") == time(13, 35)

        with pytest.raises(exc.DatetimeParseError) as info:
            v("13.35.00")
        assert info.value.expected == parser
        assert info.value.actual == "13.35.00"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("13:35")
        assert info.value.expected == time
        assert info.value.actual == str


@pytest.mark.parametrize("min", [None, time(8, 0)])
@pytest.mark.parametrize("max", [None, time(18, 0)])
def test_time_min_max(module, min, max):
    v = module.Time(min=min, max=max)
    assert v(time(13, 35)) == time(13, 35)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

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


def test_datetime(module):
    v = module.Datetime()
    today = date.today()
    now = datetime.now()
    assert v(today) == datetime.combine(today, time())
    assert v(now) == now
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v


def test_datetime_contracts(module):
    with pytest.raises(ValueError) as info:
        module.Datetime(min=datetime.now(), tz=UTC)
    assert info.value.args == (
        "%s.Datetime.min should be timezone-aware datetime object"
        % module.Datetime.__module__,
    )
    with pytest.raises(ValueError) as info:
        module.Datetime(max=datetime.now(), tz=UTC)
    assert info.value.args == (
        "%s.Datetime.max should be timezone-aware datetime object"
        % module.Datetime.__module__,
    )
    with pytest.raises(ValueError) as info:
        module.Datetime(default_time=time(7, 30), tz=UTC)
    assert info.value.args == (
        "%s.Datetime.default_time should be timezone-aware time object"
        % module.Datetime.__module__,
    )
    with pytest.raises(ValueError) as info:
        module.Datetime(min=datetime.now(UTC))
    assert info.value.args == (
        "%s.Datetime.min should be naive datetime object" % module.Datetime.__module__,
    )
    with pytest.raises(ValueError) as info:
        module.Datetime(max=datetime.now(UTC))
    assert info.value.args == (
        "%s.Datetime.max should be naive datetime object" % module.Datetime.__module__,
    )
    with pytest.raises(ValueError) as info:
        module.Datetime(default_time=time(7, 30, tzinfo=UTC))
    assert info.value.args == (
        "%s.Datetime.default_time should be naive time object"
        % module.Datetime.__module__,
    )


@pytest.mark.parametrize("nullable", [None, False, True])
def test_datetime_nullable(module, nullable):
    v = module.Datetime(nullable=nullable)
    today = date.today()
    now = datetime.now()
    assert v(today) == datetime.combine(today, time())
    assert v(now) == now
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == datetime
        assert info.value.actual == NoneType


@pytest.mark.parametrize("tz", [None, EST])
@pytest.mark.parametrize("unixts", [None, False, True])
def test_datetime_unixts(module, unixts, tz):
    v = module.Datetime(unixts=unixts, tz=tz)
    today = date.today()
    now = datetime.now() if tz is None else datetime.now(UTC).astimezone(tz)
    assert v(today) == datetime.combine(today, time(tzinfo=tz))
    assert v(now) == now
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if unixts:
        ts = timestamp()
        assert v(ts) == (
            datetime.fromtimestamp(ts)
            if tz is None
            else datetime.fromtimestamp(ts, UTC).astimezone(tz)
        )

        # Should handle ``ValueError`` on 64-bit machine
        with pytest.raises(exc.MaxValueError) as info:
            v(1 << 50)
        assert info.value.expected == platform.MAX_TIMESTAMP
        assert info.value.actual == 1 << 50

        with pytest.raises(exc.MinValueError) as info:
            v(-1 << 50)
        assert info.value.expected == platform.MIN_TIMESTAMP
        assert info.value.actual == -1 << 50

        # Should handle ``OSError`` on 64-bit machine
        with pytest.raises(exc.MaxValueError) as info:
            v(1 << 60)
        assert info.value.expected == platform.MAX_TIMESTAMP
        assert info.value.actual == 1 << 60

        with pytest.raises(exc.MinValueError) as info:
            v(-1 << 60)
        assert info.value.expected == platform.MIN_TIMESTAMP
        assert info.value.actual == -1 << 60

        # Should handle ``OverflowError`` on 64-bit machine
        with pytest.raises(exc.MaxValueError) as info:
            v(1 << 70)
        assert info.value.expected == platform.MAX_TIMESTAMP
        assert info.value.actual == 1 << 70

        with pytest.raises(exc.MinValueError) as info:
            v(-1 << 70)
        assert info.value.expected == platform.MIN_TIMESTAMP
        assert info.value.actual == -1 << 70

        with pytest.raises(exc.InvalidTypeError) as info:
            v(True)
        assert info.value.expected == datetime
        assert info.value.actual == bool
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(timestamp())
        assert info.value.expected == datetime
        assert info.value.actual == float


@pytest.mark.parametrize("tz", [None, EST])
@pytest.mark.parametrize("format", [None, "%Y-%m-%dT%H:%M"])
def test_datetime_format(module, format, tz):
    if tz is not None and format is not None:
        format += "%z"
    v = module.Datetime(format=format, tz=tz)
    today = date.today()
    now = datetime.now() if tz is None else datetime.now(UTC).astimezone(tz)
    assert v(today) == datetime.combine(today, time(tzinfo=tz))
    assert v(now) == now
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if format:
        if tz is None:
            assert v("2018-07-03T19:15") == datetime(2018, 7, 3, 19, 15)
        else:
            dt = datetime(2018, 7, 3, 19, 15, tzinfo=UTC).astimezone(tz)
            assert v("2018-07-03T19:15+0000") == dt

        with pytest.raises(exc.DatetimeParseError) as info:
            v("03.07.2018 19:15")
        assert info.value.expected == format
        assert info.value.actual == "03.07.2018 19:15"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("2018-07-03T19:15")
        assert info.value.expected == datetime
        assert info.value.actual == str


@pytest.mark.parametrize("tz", [None, EST])
@pytest.mark.parametrize("parser", [None, isoparse])
def test_datetime_parser(module, parser, tz):
    v = module.Datetime(parser=parser, tz=tz)
    today = date.today()
    now = datetime.now() if tz is None else datetime.now(UTC).astimezone(tz)
    assert v(today) == datetime.combine(today, time(tzinfo=tz))
    assert v(now) == now
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if parser:
        if tz is None:
            assert v("2018-07-03T19:15") == datetime(2018, 7, 3, 19, 15)
        else:
            dt = datetime(2018, 7, 3, 19, 15, tzinfo=UTC).astimezone(tz)
            assert v("2018-07-03T19:15Z") == dt

        with pytest.raises(exc.DatetimeParseError) as info:
            v("03.07.2018 19:15")
        assert info.value.expected == parser
        assert info.value.actual == "03.07.2018 19:15"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("2018-07-03T19:15")
        assert info.value.expected == datetime
        assert info.value.actual == str


@pytest.mark.parametrize("tz", [None, EST])
@pytest.mark.parametrize("min", [None, datetime(2018, 1, 1)])
@pytest.mark.parametrize("max", [None, datetime(2019, 1, 1)])
def test_datetime_min_max(module, min, max, tz):
    if tz is not None:
        if min is not None:
            min = min.replace(tzinfo=tz)
        if max is not None:
            max = max.replace(tzinfo=tz)
    v = module.Datetime(min=min, max=max, tz=tz)
    assert v(datetime(2018, 7, 3, tzinfo=tz)) == datetime(2018, 7, 3, tzinfo=tz)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if min is None:
        assert v(datetime(2017, 7, 3, tzinfo=tz)) == datetime(2017, 7, 3, tzinfo=tz)
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(datetime(2017, 7, 3, tzinfo=tz))
        assert info.value.expected == min
        assert info.value.actual == datetime(2017, 7, 3, tzinfo=tz)

    if max is None:
        assert v(datetime(2019, 7, 3, tzinfo=tz)) == datetime(2019, 7, 3, tzinfo=tz)
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(datetime(2019, 7, 3, tzinfo=tz))
        assert info.value.expected == max
        assert info.value.actual == datetime(2019, 7, 3, tzinfo=tz)


@pytest.mark.parametrize("tz", [None, EST])
@pytest.mark.parametrize("relmin", [None, timedelta(hours=1)])
@pytest.mark.parametrize("relmax", [None, timedelta(hours=7)])
def test_datetime_relmin_relmax(module, relmin, relmax, tz):
    v = module.Datetime(relmin=relmin, relmax=relmax, tz=tz)
    now = datetime.now() if tz is None else datetime.now(UTC).astimezone(tz)
    assert v(now + timedelta(hours=3)) == now + timedelta(hours=3)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if relmin is None:
        assert v(now) == now
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(now)
        assert info.value.expected >= now + relmin
        assert info.value.expected <= now + relmin + timedelta(seconds=1)
        assert info.value.actual == now

    if relmax is None:
        assert v(now + timedelta(hours=9)) == now + timedelta(hours=9)
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(now + timedelta(hours=9))
        assert info.value.expected >= now + relmax
        assert info.value.expected <= now + relmax + timedelta(seconds=1)
        assert info.value.actual == now + timedelta(hours=9)


@pytest.mark.parametrize("tz", [None, EST])
@pytest.mark.parametrize("default_time", [None, time(7, 30)])
def test_datetime_default_time(module, default_time, tz):
    if default_time is not None:
        default_time = default_time.replace(tzinfo=tz)
    v = module.Datetime(default_time=default_time, tz=tz)

    today = date.today()
    assert v(today) == datetime.combine(today, default_time or time(tzinfo=tz))
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v


@pytest.mark.parametrize("tz", [None, EST])
def test_datetime_tz(module, tz):
    v = module.Datetime(tz=tz)

    if tz is None:
        now = datetime.now()
        assert v(now) == now
        assert v.clone() == v
        assert pickle.loads(pickle.dumps(v)) == v

        now = datetime.now(UTC)
        with pytest.raises(exc.DatetimeTypeError) as info:
            v(now)
        assert info.value.expected == "naive"
        assert info.value.actual == now
    else:
        now = datetime.now(UTC).astimezone(tz)
        assert v(now) == now
        assert v.clone() == v
        assert pickle.loads(pickle.dumps(v)) == v

        now = datetime.now()
        with pytest.raises(exc.DatetimeTypeError) as info:
            v(now)
        assert info.value.expected == "tzaware"
        assert info.value.actual == now
