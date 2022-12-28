import re

from .. import exc
from .. import contracts
from . import abstract


class Str(abstract.Validator):
    """
    Unicode String Validator


    :param bool nullable:
        accept ``None`` as a valid value.

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

    """

    __slots__ = ("nullable", "encoding", "minlen", "maxlen", "pattern", "options")

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
        encoding = contracts.expect_str(self, "encoding", encoding, nullable=True)
        minlen = contracts.expect_length(self, "minlen", minlen, nullable=True)
        maxlen = contracts.expect_length(self, "maxlen", maxlen, nullable=True)
        pattern = contracts.expect_str(self, "pattern", pattern, nullable=True)
        options = contracts.expect_container(
            self, "options", options, nullable=True, item_type=str
        )

        setattr = object.__setattr__
        setattr(self, "nullable", nullable)
        setattr(self, "encoding", encoding)
        setattr(self, "minlen", minlen)
        setattr(self, "maxlen", maxlen)
        setattr(self, "pattern", pattern)
        setattr(self, "options", options)

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

    def __init__(
        self, nullable=False, minlen=None, maxlen=None, alias=None, replace=False
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        minlen = contracts.expect_length(self, "minlen", minlen, nullable=True)
        maxlen = contracts.expect_length(self, "maxlen", maxlen, nullable=True)

        setattr = object.__setattr__
        setattr(self, "nullable", nullable)
        setattr(self, "minlen", minlen)
        setattr(self, "maxlen", maxlen)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
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
