import sys
from datetime import date, time, datetime

from .. import exc
from .. import util
from . import abstract

if sys.version_info[0] < 3:  # pragma: no cover
    string = basestring  # noqa
else:  # pragma: no cover
    string = str


class Date(abstract.Validator):
    """
    Date Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool unixts:
        convert Unix timestamp (``int`` or ``float``) to ``date``.

    :param str format:
        try to parse ``date`` from ``str`` (Python 3.x)
        or ``basestring`` (Python 2.x),
        using ``datetime.strptime(value, self.format).date()``.

    :param callable parser:
        try to parse ``date`` from ``str`` (Python 3.x)
        or ``basestring`` (Python 2.x),
        using ``self.parser(value).date()``.

    :param date min:
        absolute lower limit.

    :param date max:
        absolute upper limit.

    :param timedelta relmin:
        relative lower limit.

    :param timedelta relmax:
        relative upper limit.

    :param tzinfo tz:
        timezone, see notes below.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``isinstance(value, (int, float))`` and ``not self.unixts``;
        * if ``not isinstance(value, date)``.

    :raises DatetimeParseError:
        * if ``datetime.strptime(value, self.format)`` raises ``ValueError``;
        * if ``self.parser(value)`` raises ``ValueError``.

    :raises MinValueError:
        * if ``value < self.min``;
        * if ``value < date.today() + self.relmin``.

    :raises MaxValueError:
        * if ``value > self.max``;
        * if ``value > date.today() + self.relmax``.


    :note:
        Relative limits are calculated adding deltas to current date,
        use negative ``relmin/relmax`` to specify date in the past.

    :note:
        It implicitly converts ``datetime`` to ``date``.
        If timezone is specified and ``datetime`` object is timezone-aware,
        it will be arranged to specified timezone first.

    :note:
        If timezone is specified,
        it will be used in conversion from Unix timestamp.
        In fact,
        it will create ``datetime`` object in UTC,
        using ``datetime.fromtimestamp(value, UTC)``.
        And then arrange it to specified timezone,
        and extract date part.

    """

    __slots__ = (
        "nullable",
        "unixts",
        "format",
        "parser",
        "min",
        "max",
        "relmin",
        "relmax",
        "tz",
    )

    def __call__(self, value):
        if value is None and self.nullable:
            return value

        if not isinstance(value, (date, datetime)):
            if isinstance(value, (int, float)) and self.unixts:
                # Value will be arranged to ``self.tz`` below.
                tz = None if self.tz is None else util.UTC
                value = datetime.fromtimestamp(value, tz)
            elif isinstance(value, string) and self.format is not None:
                try:
                    value = datetime.strptime(value, self.format)
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.format, actual=value)
            elif isinstance(value, string) and self.parser is not None:
                try:
                    value = self.parser(value)
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.parser, actual=value)
            else:
                raise exc.InvalidTypeError(expected=date, actual=type(value))

        if isinstance(value, datetime):
            # Implicitly convert ``datetime`` to ``date``,
            # but localize it first, if timezone info provided
            if value.tzinfo is not None and self.tz is not None:
                value = value.astimezone(self.tz)
            value = value.date()

        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        if self.relmin is not None or self.relmax is not None:
            today = date.today()
            if self.relmin is not None and value < today + self.relmin:
                raise exc.MinValueError(expected=today + self.relmin, actual=value)
            if self.relmax is not None and value > today + self.relmax:
                raise exc.MaxValueError(expected=today + self.relmax, actual=value)

        return value


class Time(abstract.Validator):
    """
    Time Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param str format:
        try to parse ``time`` from ``str`` (Python 3.x)
        or ``basestring`` (Python 2.x),
        using ``datetime.strptime(value, self.format).time()``.

    :param callable parser:
        try to parse ``time`` from ``str`` (Python 3.x)
        or ``basestring`` (Python 2.x),
        using ``self.parser(value).time()``.

    :param time min:
        lower limit.

    :param time max:
        upper limit.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``not isinstance(value, time)``.

    :raises DatetimeParseError:
        * if ``datetime.strptime(value, self.format)`` raises ``ValueError``;
        * if ``self.parser(value)`` raises ``ValueError``.

    :raises MinValueError:
        if ``value < self.min``.

    :raises MaxValueError:
        if ``value > self.max``.

    """

    __slots__ = ("nullable", "format", "parser", "min", "max")

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, time):
            if isinstance(value, string) and self.format is not None:
                try:
                    value = datetime.strptime(value, self.format).time()
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.format, actual=value)
            elif isinstance(value, string) and self.parser is not None:
                try:
                    value = self.parser(value).time()
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.parser, actual=value)
            else:
                raise exc.InvalidTypeError(expected=time, actual=type(value))
        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        return value


class Datetime(abstract.Validator):
    """
    Date & Time Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool unixts:
        convert Unix timestamp (``int`` or ``float``) to ``datetime``.

    :param str format:
        try to parse ``datetime`` from ``str`` (Python 3.x)
        or ``basestring`` (Python 2.x),
        using ``datetime.strptime(value, self.format)``.

    :param callable parser:
        try to parse ``datetime`` from ``str`` (Python 3.x)
        or ``basestring`` (Python 2.x),
        using ``self.parser(value)``.

    :param datetime min:
        absolute lower limit.

    :param datetime max:
        absolute upper limit.

    :param timedelta relmin:
        relative lower limit.

    :param timedelta relmax:
        relative upper limit.

    :param tzinfo tz:
        timezone.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``isinstance(value, (int, float))`` and ``not self.unixts``;
        * if ``not isinstance(value, datetime)``.

    :raises DatetimeParseError:
        * if ``datetime.strptime(value, self.format)`` raises ``ValueError``;
        * if ``self.parser(value)`` raises ``ValueError``.

    :raises DatetimeTypeError:
        * if ``self.tz is None and value.tzinfo is not None``;
        * if ``self.tz is not None and value.tzinfo is None``;

    :raises MinValueError:
        * if ``value < self.min``;
        * if ``self.tz is None and value < datetime.now() + self.relmin``.
        * if ``self.tz is not None and value < datetime.now(UTC).astimezone(self.tz) + self.relmin``.

    :raises MaxValueError:
        * if ``value > self.max``;
        * if ``self.tz is None and value > datetime.now() + self.relmax``.
        * if ``self.tz is not None and value > datetime.now(UTC).astimezone(self.tz) + self.relmax``.


    :note:
        Relative limits are calculated adding deltas to midnight of current date,
        use negative ``relmin/relmax`` to specify date and time in the past.

    """

    __slots__ = (
        "nullable",
        "unixts",
        "format",
        "parser",
        "min",
        "max",
        "relmin",
        "relmax",
        "tz",
    )

    def __init__(self, **kw):
        super(Datetime, self).__init__(**kw)
        if self.tz is not None:
            if self.min is not None:
                assert (
                    self.min.tzinfo is not None
                ), "Datetime.min should be timezone-aware datetime object"
                self.min = self.min.astimezone(self.tz)
            if self.max is not None:
                assert (
                    self.max.tzinfo is not None
                ), "Datetime.max should be timezone-aware datetime object"
                self.max = self.max.astimezone(self.tz)
        else:
            assert (
                self.min is None or self.min.tzinfo is None
            ), "Datetime.min should be naive datetime object"
            assert (
                self.max is None or self.max.tzinfo is None
            ), "Datetime.max should be naive datetime object"

    def __call__(self, value):
        if value is None and self.nullable:
            return value

        if not isinstance(value, datetime):
            if isinstance(value, date):
                # Implicitly convert ``date`` to ``datetime``
                value = datetime.combine(value, time(tzinfo=self.tz))
            elif isinstance(value, (int, float)) and self.unixts:
                # Value will be arranged to ``self.tz`` below.
                tz = None if self.tz is None else util.UTC
                value = datetime.fromtimestamp(value, tz)
            elif isinstance(value, string) and self.format is not None:
                try:
                    value = datetime.strptime(value, self.format)
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.format, actual=value)
            elif isinstance(value, string) and self.parser is not None:
                try:
                    value = self.parser(value)
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.parser, actual=value)
            else:
                raise exc.InvalidTypeError(expected=datetime, actual=type(value))

        if self.tz is not None:
            if value.tzinfo is None:
                raise exc.DatetimeTypeError(expected="tzaware", actual=value)
            value = value.astimezone(self.tz)
        else:
            if value.tzinfo is not None:
                raise exc.DatetimeTypeError(expected="naive", actual=value)

        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        if self.relmin is not None or self.relmax is not None:
            if self.tz is not None:
                now = datetime.now(util.UTC).astimezone(self.tz)
            else:
                now = datetime.now()
            if self.relmin is not None and value < now + self.relmin:
                raise exc.MinValueError(expected=now + self.relmin, actual=value)
            if self.relmax is not None and value > now + self.relmax:
                raise exc.MaxValueError(expected=now + self.relmax, actual=value)

        return value
