from collections import deque, Sequence


class ValidationError(ValueError, Sequence):
    """
    Validation Error Base Class

    :param deque context:
        error context,
        empty ``deque`` by default.

    :param \**kw:
        concrete error attributes.

    Since validators try to process as much as possible,
    they can raise multiple errors
    (wrapped by :class:`validateit.exc.SchemaError`).
    To unify handling of such errors,
    each validation error provides ``Sequence`` interface.
    It means,
    you can iterate them,
    get their length,
    get nested errors by index,
    and sort nested errors by context.

    Error context is a full path,
    that indicates where the error occurred.
    It contains mapping keys,
    sequence indexes,
    and special markers
    (see :class:`validateit.exc.Extra` and :class:`validateit.exc.Step`).

    ..  doctest:: validation_error

        >>> from validateit import exc, Dict, List, Int

        >>> schema = Dict({"foo": List(Int(max=100))})
        >>> try:
        ...     schema({"foo": [1, 2, 200, 250], "bar": None})
        ... except exc.ValidationError as e:
        ...     error = e

        >>> error.sort()
        >>> error
        <SchemaError(errors=[
            <bar: ForbiddenKeyError()>,
            <foo.2: MaxValueError(expected=100, actual=200)>,
            <foo.3: MaxValueError(expected=100, actual=250)>
        ])>

        >>> len(error)
        3

        >>> error[1]
        <foo.2: MaxValueError(expected=100, actual=200)>
        >>> error[1].context
        deque(['foo', 2])
        >>> error[1].format_context()
        'foo.2'
        >>> error[1].format_error()
        'MaxValueError(expected=100, actual=200)'

        >>> error.sort(reverse=True)
        >>> error
        <SchemaError(errors=[
            <foo.3: MaxValueError(expected=100, actual=250)>,
            <foo.2: MaxValueError(expected=100, actual=200)>,
            <bar: ForbiddenKeyError()>
        ])>

    """

    __slots__ = ("context",)

    def __init__(self, context=None, **kw):
        self.context = context or deque()
        for slot, value in kw.items():
            setattr(self, slot, value)
        super(ValidationError, self).__init__(
            *(getattr(self, slot) for slot in self.__slots__)
        )

    def add_context(self, node):
        """
        Add error context

        :param node:
            key or index of member,
            where error is raised.

        :returns:
            the error itself,
            so that the method is suitable for chaining.

        Example:

        ..  doctest:: add_context

            >>> from validateit.exc import ValidationError

            >>> e = ValidationError()
            >>> e
            <ValidationError()>
            >>> e.context
            deque([])

            >>> e.add_context("foo")
            <foo: ValidationError()>
            >>> e.context
            deque(['foo'])

        """
        self.context.appendleft(node)
        return self

    def __getitem__(self, index):
        if index != 0:
            raise IndexError(index)
        return self

    def __len__(self):
        return 1

    def __iter__(self):
        yield self

    def sort(self, key=None, reverse=False):
        pass

    def __repr__(self):
        if self.context:
            return "<%s: %s>" % (self.format_context(), self.format_error())
        else:
            return "<%s>" % self.format_error()

    def __str__(self):
        return repr(self)

    def format_context(self):
        def context():
            for node in self.context:
                if isinstance(node, str) and "." in node:
                    yield "[%s]" % node
                else:
                    yield str(node)

        return ".".join(context())

    def format_error(self):
        def params():
            for slot in self.__slots__[1:]:  # Exclude ``context``
                yield "%s=%r" % (slot, getattr(self, slot))

        return "%s(%s)" % (self.__class__.__name__, ", ".join(params()))


class ConditionError(ValidationError):
    """
    Base Class for Condition Errors

    It has a couple of attributes ``expected`` and ``actual``,
    that gives info of what happens and why the error is raised.

    See derived classes for details.

    """

    __slots__ = ValidationError.__slots__ + ("expected", "actual")


class InvalidTypeError(ConditionError):
    """
    Invalid Type Error

    :param type expected:
        expected type (types).
    :type expected: type or tuple

    :param type actual:
        actual type of value.

    """

    __slots__ = ConditionError.__slots__


class OptionsError(ConditionError):
    """
    Options Error

    :param expected:
        list of valid values.
    :type expected: list or tuple

    :param actual:
        actual value.

    """

    __slots__ = ConditionError.__slots__


class MinValueError(ConditionError):
    """
    Minimum Value Error

    :param expected:
        minimal allowed value.

    :param actual:
        actual value.

    """

    __slots__ = ConditionError.__slots__


class MaxValueError(ConditionError):
    """
    Maximum Value Error

    :param expected:
        maximal allowed value.

    :param actual:
        actual value.

    """

    __slots__ = ConditionError.__slots__


class FloatValueError(ConditionError):
    """
    Float Value Error

    :param str expected:
        * ``"number"`` on test for ``Not-a-Number``;
        * ``"finite"`` on test for ``Infinity``.

    :param float actual:
        actual value.

    """

    __slots__ = ConditionError.__slots__


class StrDecodeError(ConditionError):
    """
    String Decode Error

    :param str expected:
        encoding name.

    :param bytes actual:
        actual byte-string value.

    """

    __slots__ = ConditionError.__slots__


class MinLengthError(ConditionError):
    """
    Minimum Length Error

    :param int expected:
        minimal allowed length.

    :param int actual:
        actual value length.

    """

    __slots__ = ConditionError.__slots__


class MaxLengthError(ConditionError):
    """
    Maximum Length Error

    :param int expected:
        maximal allowed length.

    :param int actual:
        actual value length.

    """

    __slots__ = ConditionError.__slots__


class TupleLengthError(ConditionError):
    """
    Tuple Length Error

    :param int expected:
        tuple length.

    :param int actual:
        actual value length.

    """

    __slots__ = ConditionError.__slots__


class PatternMatchError(ConditionError):
    """
    Pattern Match Error

    :param str expected:
        pattern, i.e. regular expression.

    :param str actual:
        actual value.

    """

    __slots__ = ConditionError.__slots__


class DatetimeParseError(ConditionError):
    """
    Date & Time Parse Error

    :param str expected:
        format.

    :param str actual:
        actual value.

    """

    __slots__ = ConditionError.__slots__


class RecursionMaxDepthError(ConditionError):
    """
    Recursion Maximum Depth Error

    :param int expected:
        maximal allowed depth.

    :param int actual:
        actual recursion depth.

    """

    __slots__ = ConditionError.__slots__


class MappingKeyError(ValidationError):
    """
    Base Class for Mapping Key Errors

    :param key:
        failed key,
        that goes into error context.

    ..  testsetup:: mapping_key_error

        from validateit.exc import MappingKeyError

    ..  doctest:: mapping_key_error

        >>> e = MappingKeyError("foo")
        >>> e
        <foo: MappingKeyError()>

    """

    __slots__ = ValidationError.__slots__

    def __init__(self, key, **kw):
        super(MappingKeyError, self).__init__(context=deque([key]), **kw)


class ForbiddenKeyError(MappingKeyError):
    """Forbidden Mapping Key Error"""

    __slots__ = MappingKeyError.__slots__


class MissingKeyError(MappingKeyError):
    """Missing Mapping Key Error"""

    __slots__ = MappingKeyError.__slots__


class SchemaError(ValidationError):
    """
    Schema Error

    It is an error class,
    that wraps multiple errors occurred during complex structure validation.

    :param list errors:
        list of all errors occurred during complex structure validation.

    """

    __slots__ = ValidationError.__slots__ + ("errors",)

    def __init__(self, errors):
        super(SchemaError, self).__init__(errors=errors)

    def __getitem__(self, index):
        return self.errors[index]

    def __len__(self):
        return len(self.errors)

    def __iter__(self):
        for error in self.errors:
            yield error

    def sort(self, key=None, reverse=False):
        if key is None:
            key = lambda error: tuple(repr(node) for node in error.context)
        self.errors.sort(key=key, reverse=reverse)

    def __repr__(self):
        errors = ",\n".join("    %r" % e for e in self.errors)
        return "<%s(errors=[\n%s\n])>" % (self.__class__.__name__, errors)

    def add_context(self, node):
        for e in self.errors:
            e.add_context(node)
        return self


class Extra(object):
    """
    Extra Key Context Marker

    It is a special context marker,
    that is used by mapping validators to indicate,
    which part of extra key/value pair is failed.

    There are two constants in the module:

    *   ``EXTRA_KEY`` indicates that key validation is failed;
    *   ``EXTRA_VALUE`` indicates that value validation is failed.

    It has special representation,
    to be easily distinguished from other string keys.

    :param str name:
        name of pair part,
        i.e. ``KEY`` or ``VALUE``.

    ..  doctest:: extra

        >>> from validateit import exc, Dict, Str

        >>> schema = Dict(extra=(Str(maxlen=2), Str(maxlen=4)))
        >>> try:
        ...     schema({"xy": "abc", "xyz": "abcde"})
        ... except exc.ValidationError as e:
        ...     error = e

        >>> error
        <SchemaError(errors=[
            <xyz.@KEY: MaxLengthError(expected=2, actual=3)>,
            <xyz.@VALUE: MaxLengthError(expected=4, actual=5)>
        ])>

        >>> repr(error.errors[0].context[1])
        '@KEY'
        >>> error.errors[0].context[1].name
        'KEY'

        >>> error.errors[0].context[1] is exc.EXTRA_KEY
        True
        >>> error.errors[1].context[1] is exc.EXTRA_VALUE
        True

    """

    __slots__ = ("name",)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "@%s" % self.name

    def __eq__(self, other):
        return self.__class__ is type(other) and self.name == other.name


EXTRA_KEY = Extra("KEY")
EXTRA_VALUE = Extra("VALUE")


class Step(object):
    """
    Step Number Context Marker

    It is a special context marker,
    that is used by pipeline validators to indicate,
    which validation step is failed.
    It has special representation,
    to be easily distinguished from sequence indexes.

    :param int num:
        number of failed step.

    ..  doctest:: step

        >>> from validateit import exc, OneOf, Int

        >>> schema = OneOf(Int(min=0, max=10), Int(min=90, max=100))
        >>> try:
        ...     schema(50)
        ... except exc.ValidationError as e:
        ...     error = e

        >>> error
        <SchemaError(errors=[
            <#0: MaxValueError(expected=10, actual=50)>,
            <#1: MinValueError(expected=90, actual=50)>
        ])>

        >>> repr(error.errors[0].context[0])
        '#0'
        >>> error.errors[0].context[0].num
        0
        >>> isinstance(error.errors[0].context[0], exc.Step)
        True

    """

    __slots__ = ("num",)

    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return "#%s" % self.num

    def __eq__(self, other):
        return self.__class__ is type(other) and self.num == other.num
