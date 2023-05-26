from datetime import date, time, datetime, timedelta, timezone, tzinfo

from .. import exc
from .. import contracts
from .. import platform
from . cimport abstract


cdef class Date(abstract.Validator):
    """
    Date Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool unixts:
        convert Unix timestamp (``int`` or ``float``) to ``date``.

    :param str format:
        try to parse ``date`` from ``str``
        using ``datetime.strptime(value, self.format).date()``.

    :param callable parser:
        try to parse ``date`` from ``str``
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
        * if ``isinstance(value, bool) and self.unixts``,
          because ``issubclass(bool, int) is True``,
          but it is very unlikely ``bool`` could represent a valid timestamp;
        * if ``not isinstance(value, date)``.

    :raises DatetimeParseError:
        * if ``datetime.strptime(value, self.format)`` raises ``ValueError``;
        * if ``self.parser(value)`` raises ``ValueError``.

    :raises MinValueError:
        * if ``value < self.min``;
        * if ``value < date.today() + self.relmin``;
        * if ``self.unixts`` and value lesser than the minimal supported timestamp.

    :raises MaxValueError:
        * if ``value > self.max``;
        * if ``value > date.today() + self.relmax``;
        * if ``self.unixts`` and value greater than the maximal supported timestamp.


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
        It also will be used in the same way
        to get ``today`` value for ``relmin/relmax`` checks,
        i.e. ``datetime.now(UTC).astimezone(self.tz).date()``.

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

    cdef bint _nullable
    cdef bint _unixts
    cdef str _format
    cdef object _parser
    cdef object _min
    cdef object _max
    cdef object _relmin
    cdef object _relmax
    cdef object _tz

    @property
    def nullable(self):
        return self._nullable

    @property
    def unixts(self):
        return self._unixts

    @property
    def format(self):
        return self._format

    @property
    def parser(self):
        return self._parser

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def relmin(self):
        return self._relmin

    @property
    def relmax(self):
        return self._relmax

    @property
    def tz(self):
        return self._tz

    def __init__(
        self,
        nullable=False,
        unixts=False,
        format=None,
        parser=None,
        min=None,
        max=None,
        relmin=None,
        relmax=None,
        tz=None,
        alias=None,
        replace=False,
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        unixts = contracts.expect_flag(self, "unixts", unixts)
        format = contracts.expect_str(self, "format", format, nullable=True)
        parser = contracts.expect_callable(self, "parser", parser, nullable=True)
        min = contracts.expect(self, "min", min, types=date, nullable=True)
        max = contracts.expect(self, "max", max, types=date, nullable=True)
        relmin = contracts.expect(
            self, "relmin", relmin, types=timedelta, nullable=True
        )
        relmax = contracts.expect(
            self, "relmax", relmax, types=timedelta, nullable=True
        )
        tz = contracts.expect(self, "tz", tz, types=tzinfo, nullable=True)

        self._nullable = nullable
        self._unixts = unixts
        self._format = format
        self._parser = parser
        self._min = min
        self._max = max
        self._relmin = relmin
        self._relmax = relmax
        self._tz = tz

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self.nullable:
            return value

        if not isinstance(value, (date, datetime)):
            if (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and self.unixts
            ):
                # Value will be arranged to ``self.tz`` below.
                tz = None if self.tz is None else timezone.utc
                try:
                    value = datetime.fromtimestamp(value, tz)
                except (ValueError, OSError, OverflowError):
                    raise (
                        exc.MaxValueError(
                            expected=platform.MAX_TIMESTAMP,
                            actual=value,
                        )
                        if value > 0
                        else exc.MinValueError(
                            expected=platform.MIN_TIMESTAMP,
                            actual=value,
                        )
                    )
            elif isinstance(value, str) and self.format is not None:
                try:
                    value = datetime.strptime(value, self.format)
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.format, actual=value)
            elif isinstance(value, str) and self.parser is not None:
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
            if self.tz is not None:
                today = datetime.now(timezone.utc).astimezone(self.tz).date()
            else:
                today = date.today()
            if self.relmin is not None and value < today + self.relmin:
                raise exc.MinValueError(expected=today + self.relmin, actual=value)
            if self.relmax is not None and value > today + self.relmax:
                raise exc.MaxValueError(expected=today + self.relmax, actual=value)

        return value


cdef class Time(abstract.Validator):
    """
    Time Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param str format:
        try to parse ``time`` from ``str``
        using ``datetime.strptime(value, self.format).time()``.

    :param callable parser:
        try to parse ``time`` from ``str``
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

    cdef bint _nullable
    cdef str _format
    cdef object _parser
    cdef object _min
    cdef object _max

    @property
    def nullable(self):
        return self._nullable

    @property
    def format(self):
        return self._format

    @property
    def parser(self):
        return self._parser

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    def __init__(
        self,
        nullable=False,
        format=None,
        parser=None,
        min=None,
        max=None,
        alias=None,
        replace=False,
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        format = contracts.expect_str(self, "format", format, nullable=True)
        parser = contracts.expect_callable(self, "parser", parser, nullable=True)
        min = contracts.expect(self, "min", min, types=time, nullable=True)
        max = contracts.expect(self, "max", max, types=time, nullable=True)

        self._nullable = nullable
        self._format = format
        self._parser = parser
        self._min = min
        self._max = max

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self.nullable:
            return value
        if not isinstance(value, time):
            if isinstance(value, str) and self.format is not None:
                try:
                    value = datetime.strptime(value, self.format).time()
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.format, actual=value)
            elif isinstance(value, str) and self.parser is not None:
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


cdef class Datetime(abstract.Validator):
    """
    Date & Time Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool unixts:
        convert Unix timestamp (``int`` or ``float``) to ``datetime``.

    :param str format:
        try to parse ``datetime`` from ``str``
        using ``datetime.strptime(value, self.format)``.

    :param callable parser:
        try to parse ``datetime`` from ``str``
        using ``self.parser(value)``.

    :param datetime min:
        absolute lower limit.

    :param datetime max:
        absolute upper limit.

    :param timedelta relmin:
        relative lower limit.

    :param timedelta relmax:
        relative upper limit.

    :param time default_time:
        is used to implicitly convert ``date`` to ``datetime``
        using ``datetime.combine(value, self.default_time or time(tzinfo=self.tz))``.

    :param tzinfo tz:
        timezone.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``isinstance(value, (int, float))`` and ``not self.unixts``;
        * if ``isinstance(value, bool) and self.unixts``,
          because ``issubclass(bool, int) is True``,
          but it is very unlikely ``bool`` could represent a valid timestamp;
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
        * if ``self.tz is not None and value < datetime.now(UTC).astimezone(self.tz) + self.relmin``;
        * if ``self.unixts`` and value lesser than the minimal supported timestamp.

    :raises MaxValueError:
        * if ``value > self.max``;
        * if ``self.tz is None and value > datetime.now() + self.relmax``.
        * if ``self.tz is not None and value > datetime.now(UTC).astimezone(self.tz) + self.relmax``;
        * if ``self.unixts`` and value greater than the maximal supported timestamp.

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
        "default_time",
        "tz",
    )

    cdef bint _nullable
    cdef bint _unixts
    cdef str _format
    cdef object _parser
    cdef object _min
    cdef object _max
    cdef object _relmin
    cdef object _relmax
    cdef object _default_time
    cdef object _tz

    @property
    def nullable(self):
        return self._nullable

    @property
    def unixts(self):
        return self._unixts

    @property
    def format(self):
        return self._format

    @property
    def parser(self):
        return self._parser

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def relmin(self):
        return self._relmin

    @property
    def relmax(self):
        return self._relmax

    @property
    def default_time(self):
        return self._default_time

    @property
    def tz(self):
        return self._tz

    def __init__(
        self,
        nullable=False,
        unixts=False,
        format=None,
        parser=None,
        min=None,
        max=None,
        relmin=None,
        relmax=None,
        default_time=None,
        tz=None,
        alias=None,
        replace=False,
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        unixts = contracts.expect_flag(self, "unixts", unixts)
        format = contracts.expect_str(self, "format", format, nullable=True)
        parser = contracts.expect_callable(self, "parser", parser, nullable=True)
        min = contracts.expect(self, "min", min, types=datetime, nullable=True)
        max = contracts.expect(self, "max", max, types=datetime, nullable=True)
        relmin = contracts.expect(
            self, "relmin", relmin, types=timedelta, nullable=True
        )
        relmax = contracts.expect(
            self, "relmax", relmax, types=timedelta, nullable=True
        )
        default_time = contracts.expect(
            self, "default_time", default_time, types=time, nullable=True
        )
        tz = contracts.expect(self, "tz", tz, types=tzinfo, nullable=True)

        if tz is not None:
            if min is not None:
                if min.tzinfo is None:
                    raise ValueError(
                        "%s.%s.min should be timezone-aware datetime object"
                        % (self.__class__.__module__, self.__class__.__name__)
                    )
                min = min.astimezone(tz)
            if max is not None:
                if max.tzinfo is None:
                    raise ValueError(
                        "%s.%s.max should be timezone-aware datetime object"
                        % (self.__class__.__module__, self.__class__.__name__)
                    )
                max = max.astimezone(tz)
            if default_time is not None:
                if default_time.tzinfo is None:
                    raise ValueError(
                        "%s.%s.default_time should be timezone-aware time object"
                        % (self.__class__.__module__, self.__class__.__name__)
                    )
        else:
            if min is not None and min.tzinfo is not None:
                raise ValueError(
                    "%s.%s.min should be naive datetime object"
                    % (self.__class__.__module__, self.__class__.__name__)
                )
            if max is not None and max.tzinfo is not None:
                raise ValueError(
                    "%s.%s.max should be naive datetime object"
                    % (self.__class__.__module__, self.__class__.__name__)
                )
            if default_time is not None and default_time.tzinfo is not None:
                raise ValueError(
                    "%s.%s.default_time should be naive time object"
                    % (self.__class__.__module__, self.__class__.__name__)
                )

        self._nullable = nullable
        self._unixts = unixts
        self._format = format
        self._parser = parser
        self._min = min
        self._max = max
        self._relmin = relmin
        self._relmax = relmax
        self._default_time = default_time
        self._tz = tz

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self.nullable:
            return value

        if not isinstance(value, datetime):
            if isinstance(value, date):
                # Implicitly convert ``date`` to ``datetime``
                value = datetime.combine(
                    value,
                    self.default_time or time(tzinfo=self.tz),
                )
            elif (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and self.unixts
            ):
                # Value will be arranged to ``self.tz`` below.
                tz = None if self.tz is None else timezone.utc
                try:
                    value = datetime.fromtimestamp(value, tz)
                except (ValueError, OSError, OverflowError):
                    raise (
                        exc.MaxValueError(
                            expected=platform.MAX_TIMESTAMP,
                            actual=value,
                        )
                        if value > 0
                        else exc.MinValueError(
                            expected=platform.MIN_TIMESTAMP,
                            actual=value,
                        )
                    )
            elif isinstance(value, str) and self.format is not None:
                try:
                    value = datetime.strptime(value, self.format)
                except ValueError:
                    raise exc.DatetimeParseError(expected=self.format, actual=value)
            elif isinstance(value, str) and self.parser is not None:
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
                now = datetime.now(timezone.utc).astimezone(self.tz)
            else:
                now = datetime.now()
            if self.relmin is not None and value < now + self.relmin:
                raise exc.MinValueError(expected=now + self.relmin, actual=value)
            if self.relmax is not None and value > now + self.relmax:
                raise exc.MaxValueError(expected=now + self.relmax, actual=value)

        return value
