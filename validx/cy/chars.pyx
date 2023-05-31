from libc cimport limits
import re

from .. import exc
from .. import contracts
from . cimport abstract


cdef class Str(abstract.Validator):
    """
    Unicode String Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool coerce:
        convert non-string value to ``str``,
        **use with caution** (see notes below).

    :param bool dontstrip:
        do not strip leading & trailing whitespace.

    :param bool normspace:
        normalize spaces, i.e. replace any space sequence by single space char.

    :param str encoding:
        try to decode ``bytes`` to ``str`` using specified encoding.

    :param int minlen:
        lower length limit.

    :param int maxlen:
        upper length limit.

    :param str pattern:
        validate string using regular expression.

    :param iterable options:
        explicit enumeration of valid values.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``not isinstance(value, str)``.

    :raises StrDecodeError:
        if ``value.decode(self.encoding)`` raises ``UnicodeDecodeError``.

    :raises MinLengthError:
        if ``len(value) < self.minlen``.

    :raises MaxLengthError:
        if ``len(value) > self.maxlen``.

    :raises PatternMatchError:
        if ``value`` does not match ``self.pattern``.

    :raises OptionsError:
        if ``value not in self.options``.


    :note:
        Since any Python object can be converted to a string,
        using ``coerce`` without other checks in fact validates nothing.
        It can be useful though to sanitize data from sources with automatic type inferring,
        where string data might be incorrectly interpreted as another type.
        For example, phone number as ``int``, version number as ``float``, etc.

    """

    __slots__ = (
        "nullable",
        "coerce",
        "dontstrip",
        "normspace",
        "encoding",
        "minlen",
        "maxlen",
        "pattern",
        "options",
    )

    cdef bint _nullable
    cdef bint _coerce
    cdef bint _dontstrip
    cdef bint _normspace
    cdef str _encoding
    cdef long _minlen
    cdef long _maxlen
    cdef str _pattern
    cdef frozenset _options

    @property
    def nullable(self):
        return self._nullable

    @property
    def coerce(self):
        return self._coerce

    @property
    def dontstrip(self):
        return self._dontstrip

    @property
    def normspace(self):
        return self._normspace

    @property
    def encoding(self):
        return self._encoding

    @property
    def minlen(self):
        return None if self._minlen == 0 else self._minlen

    @property
    def maxlen(self):
        return None if self._maxlen == limits.LONG_MAX else self._maxlen

    @property
    def pattern(self):
        return self._pattern

    @property
    def options(self):
        return self._options

    def __init__(
        self,
        nullable=False,
        coerce=False,
        dontstrip=False,
        normspace=False,
        encoding=None,
        minlen=None,
        maxlen=None,
        pattern=None,
        options=None,
        alias=None,
        replace=False,
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        coerce = contracts.expect_flag(self, "coerce", coerce)
        dontstrip = contracts.expect_flag(self, "dontstrip", dontstrip)
        normspace = contracts.expect_flag(self, "normspace", normspace)
        encoding = contracts.expect_str(self, "encoding", encoding, nullable=True)
        minlen = contracts.expect_length(self, "minlen", minlen, nullable=True)
        maxlen = contracts.expect_length(self, "maxlen", maxlen, nullable=True)
        pattern = contracts.expect_str(self, "pattern", pattern, nullable=True)
        options = contracts.expect_container(
            self, "options", options, nullable=True, item_type=str
        )

        self._nullable = nullable
        self._coerce = coerce
        self._dontstrip = dontstrip
        self._normspace = normspace
        self._encoding = encoding
        self._minlen = 0 if minlen is None else minlen
        self._maxlen = limits.LONG_MAX if maxlen is None else maxlen
        self._pattern = pattern
        self._options = options

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self.nullable:
            return value
        if not isinstance(value, str):
            if isinstance(value, bytes) and self.encoding is not None:
                try:
                    value = value.decode(self.encoding)
                except UnicodeDecodeError:
                    raise exc.StrDecodeError(expected=self.encoding, actual=value)
            elif self.coerce:
                value = str(value)
            else:
                raise exc.InvalidTypeError(expected=str, actual=type(value))
        if not self.dontstrip:
            value = value.strip()
        if self.normspace:
            value = re.sub(r"\s+", " ", value)
        cdef long length = len(value)
        if length < self._minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if length > self._maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)
        if self.pattern and not re.match(self.pattern, value):
            raise exc.PatternMatchError(expected=self.pattern, actual=value)
        if self.options is not None and value not in self.options:
            raise exc.OptionsError(expected=self.options, actual=value)
        return value


cdef class Bytes(abstract.Validator):
    """
    Byte String Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param int minlen:
        lower length limit.

    :param int maxlen:
        upper length limit.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``not isinstance(value, bytes)``.

    :raises MinLengthError:
        if ``len(value) < self.minlen``.

    :raises MaxLengthError:
        if ``len(value) > self.maxlen``.

    """

    __slots__ = ("nullable", "minlen", "maxlen")

    cdef bint _nullable
    cdef long _minlen
    cdef long _maxlen

    @property
    def nullable(self):
        return self._nullable

    @property
    def minlen(self):
        return None if self._minlen == 0 else self._minlen

    @property
    def maxlen(self):
        return None if self._maxlen == limits.LONG_MAX else self._maxlen

    def __init__(
        self, nullable=False, minlen=None, maxlen=None, alias=None, replace=False
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        minlen = contracts.expect_length(self, "minlen", minlen, nullable=True)
        maxlen = contracts.expect_length(self, "maxlen", maxlen, nullable=True)

        self._nullable = nullable
        self._minlen = 0 if minlen is None else minlen
        self._maxlen = limits.LONG_MAX if maxlen is None else maxlen

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self._nullable:
            return value
        if not isinstance(value, bytes):
            raise exc.InvalidTypeError(expected=bytes, actual=type(value))
        cdef long length = len(value)
        if length < self._minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if length > self._maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)
        return value
