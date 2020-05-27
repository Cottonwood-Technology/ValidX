from libc cimport limits
import re

from .. import exc
from .. import contracts
from ..compat.types import string
from . cimport abstract


cdef class Str(abstract.Validator):
    """
    Unicode String Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param str encoding:
        try to decode byte-string to ``str/unicode``,
        using specified encoding.

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
        * if ``not isinstance(value, str)`` (Python 3.x)
          or ``not isinstance(value, unicode)`` (Python 2.x).

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

    """

    __slots__ = ("nullable", "encoding", "minlen", "maxlen", "pattern", "options")

    cdef bint _nullable
    cdef basestring _encoding
    cdef long _minlen
    cdef long _maxlen
    cdef basestring _pattern
    cdef frozenset _options

    @property
    def nullable(self):
        return self._nullable

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
        encoding=None,
        minlen=None,
        maxlen=None,
        pattern=None,
        options=None,
        alias=None,
        replace=False,
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        encoding = contracts.expect_basestr(self, "encoding", encoding, nullable=True)
        minlen = contracts.expect_length(self, "minlen", minlen, nullable=True)
        maxlen = contracts.expect_length(self, "maxlen", maxlen, nullable=True)
        pattern = contracts.expect_basestr(self, "pattern", pattern, nullable=True)
        options = contracts.expect_container(
            self, "options", options, nullable=True, item_type=string
        )

        self._nullable = nullable
        self._encoding = encoding
        self._minlen = 0 if minlen is None else minlen
        self._maxlen = limits.LONG_MAX if maxlen is None else maxlen
        self._pattern = pattern
        self._options = options

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self.nullable:
            return value
        if not isinstance(value, string):
            if isinstance(value, bytes) and self.encoding is not None:
                try:
                    value = value.decode(self.encoding)
                except UnicodeDecodeError:
                    raise exc.StrDecodeError(expected=self.encoding, actual=value)
            else:
                raise exc.InvalidTypeError(expected=string, actual=type(value))
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
