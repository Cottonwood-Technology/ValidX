import re
import sys

from .. import exc
from . import abstract


if sys.version_info[0] < 3:  # pragma: no cover
    str = unicode  # noqa


class Str(abstract.Validator):

    __slots__ = ("nullable", "encoding", "minlen", "maxlen", "pattern", "options")

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, str):
            if isinstance(value, bytes) and self.encoding is not None:
                try:
                    value = value.decode(self.encoding)
                except UnicodeDecodeError:
                    raise exc.StrDecodeError(expected=self.encoding, actual=value)
            else:
                raise exc.InvalidTypeError(expected=str, actual=type(value))
        length = len(value)
        if self.minlen is not None and length < self.minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if self.maxlen is not None and length > self.maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)
        if self.pattern and not re.match(self.pattern, value):
            raise exc.PatternMatchError(expected=self.pattern, actual=value)
        if self.options is not None and value not in self.options:
            raise exc.OptionsError(expected=self.options, actual=value)
        return value


class Bytes(abstract.Validator):

    __slots__ = ("nullable", "minlen", "maxlen")

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, bytes):
            raise exc.InvalidTypeError(expected=bytes, actual=type(value))
        length = len(value)
        if self.minlen is not None and length < self.minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if self.maxlen is not None and length > self.maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)
        return value
