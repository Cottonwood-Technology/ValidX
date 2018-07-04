import sys
from datetime import date, time, datetime

from .. import exc
from . import abstract

if sys.version_info[0] < 3:  # pragma: no cover
    string = basestring  # noqa
else:  # pragma: no cover
    string = str


class Date(abstract.Validator):

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
