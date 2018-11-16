import sys
from datetime import date, time, datetime

from .. import exc
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
        using specified format.

    :param date min:
        absolute lower limit.

    :param date max:
        absolute upper limit.

    :param timedelta relmin:
        relative lower limit.

    :param timedelta relmax:
        relative upper limit.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``isinstance(value, (int, float))`` and ``not self.unixts``;
        * if ``not isinstance(value, date)``.

    :raises DatetimeParseError:
        when ``datetime.strptime(value, self.format)`` raises ``ValueError``.

    :raises MinValueError:
        * if ``value < self.min``;
        * if ``value < date.today() + self.relmin``.

    :raises MaxValueError:
        * if ``value > self.max``;
        * if ``value > date.today() + self.relmax``.


    :note:
        Relative limits are calculated adding deltas to current date,
        use negative ``relmin/relmax`` to specify date in the past.

    """

    __slots__ = ("nullable", "unixts", "format", "min", "max", "relmin", "relmax")

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if isinstance(value, datetime):
            # Implicitly convert ``datetime`` to ``date``
            value = value.date()
        if not isinstance(value, date):
            if isinstance(value, (int, float)) and self.unixts:
                value = date.fromtimestamp(value)
            elif isinstance(value, string) and self.format is not None:
                try:
                    value = datetime.strptime(value, self.format).date()
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.format, actual=value)
            else:
                raise exc.InvalidTypeError(expected=date, actual=type(value))
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
        using specified format.

    :param time min:
        lower limit.

    :param time max:
        upper limit.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``not isinstance(value, time)``.

    :raises DatetimeParseError:
        when ``datetime.strptime(value, self.format)`` raises ``ValueError``.

    :raises MinValueError:
        if ``value < self.min``.

    :raises MaxValueError:
        if ``value > self.max``.

    """

    __slots__ = ("nullable", "format", "min", "max")

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, time):
            if isinstance(value, string) and self.format is not None:
                try:
                    value = datetime.strptime(value, self.format).time()
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.format, actual=value)
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
        using specified format.

    :param datetime min:
        absolute lower limit.

    :param datetime max:
        absolute upper limit.

    :param timedelta relmin:
        relative lower limit.

    :param timedelta relmax:
        relative upper limit.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``isinstance(value, (int, float))`` and ``not self.unixts``;
        * if ``not isinstance(value, datetime)``.

    :raises DatetimeParseError:
        when ``datetime.strptime(value, self.format)`` raises ``ValueError``.

    :raises MinValueError:
        * if ``value < self.min``;
        * if ``value < datetime.combine(date.today(), time()) + self.relmin``.

    :raises MaxValueError:
        * if ``value > self.max``;
        * if ``value > datetime.combine(date.today(), time()) + self.relmax``.


    :note:
        Relative limits are calculated adding deltas to midnight of current date,
        use negative ``relmin/relmax`` to specify date and time in the past.

    """

    __slots__ = ("nullable", "unixts", "format", "min", "max", "relmin", "relmax")

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, datetime):
            if isinstance(value, date):
                # Implicitly convert ``date`` to ``datetime``
                value = datetime.combine(value, time())
            elif isinstance(value, (int, float)) and self.unixts:
                value = datetime.fromtimestamp(value)
            elif isinstance(value, string) and self.format is not None:
                try:
                    value = datetime.strptime(value, self.format)
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.format, actual=value)
            else:
                raise exc.InvalidTypeError(expected=datetime, actual=type(value))
        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        if self.relmin is not None or self.relmax is not None:
            today = datetime.combine(date.today(), time())
            if self.relmin is not None and value < today + self.relmin:
                raise exc.MinValueError(expected=today + self.relmin, actual=value)
            if self.relmax is not None and value > today + self.relmax:
                raise exc.MaxValueError(expected=today + self.relmax, actual=value)
        return value
