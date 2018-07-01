from libc cimport limits
import re

from .. import exc
from . cimport abstract


cdef class Str(abstract.Validator):

    __slots__ = ("nullable", "encoding", "minlen", "maxlen", "pattern", "options")

    cdef public bint nullable
    cdef public str encoding
    cdef long _minlen
    cdef long _maxlen
    cdef public pattern
    cdef public options

    @property
    def minlen(self):
        return None if self._minlen == 0 else self._minlen

    @minlen.setter
    def minlen(self, value):
        self._minlen = value if value is not None else 0

    @property
    def maxlen(self):
        return None if self._maxlen == limits.LONG_MAX else self._maxlen

    @maxlen.setter
    def maxlen(self, value):
        self._maxlen = value if value is not None else limits.LONG_MAX

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, unicode):
            if isinstance(value, bytes) and self.encoding is not None:
                try:
                    value = value.decode(self.encoding)
                except UnicodeDecodeError:
                    raise exc.StrDecodeError(expected=self.encoding, actual=value)
            else:
                raise exc.InvalidTypeError(expected=unicode, actual=type(value))
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

    __slots__ = ("nullable", "minlen", "maxlen")

    cdef public nullable
    cdef long _minlen
    cdef long _maxlen

    @property
    def minlen(self):
        return None if self._minlen == 0 else self._minlen

    @minlen.setter
    def minlen(self, value):
        self._minlen = value if value is not None else 0

    @property
    def maxlen(self):
        return None if self._maxlen == limits.LONG_MAX else self._maxlen

    @maxlen.setter
    def maxlen(self, value):
        self._maxlen = value if value is not None else limits.LONG_MAX

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, bytes):
            raise exc.InvalidTypeError(expected=bytes, actual=type(value))
        cdef long length = len(value)
        if length < self._minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if length > self._maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)
        return value
