class ValidationError(ValueError):
    """
    Validation Error Base Class

    :param list context:
        error context,
        empty list by default.

    :param \**kw:
        concrete error attributes.

    Each validation error has its context,
    that indicates which member of validating structure is failed.

    ..  testsetup:: exc

        from validateit import Dict, List, Int
        from validateit.exc import ValidationError

    ..  doctest:: exc

        >>> schema = Dict({"foo": List(Int(max=100))})
        >>> try:
        ...     schema({"foo": [1, 2, 200, 250]})
        ... except ValidationError as e:
        ...     error = e

        >>> error
        <SchemaError(errors=[
            <foo.2: MaxValueError(expected=100, actual=200)>,
            <foo.3: MaxValueError(expected=100, actual=250)>
        ])>

        >>> error.errors[0].context
        ['foo', 2]

        >>> error.errors[1].context
        ['foo', 3]


    Each validation error is iterable.
    It unifies handling of single and composite errors:

    ..  doctest:: exc

        >>> for e in error:
        ...     print(e)
        <foo.2: MaxValueError(expected=100, actual=200)>
        <foo.3: MaxValueError(expected=100, actual=250)>

        >>> for e in error.errors[0]:
        ...     print(e)
        <foo.2: MaxValueError(expected=100, actual=200)>


    """

    __slots__ = ("context",)

    def __init__(self, **kw):
        kw.setdefault("context", [])
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

        ..  testsetup:: add_context

            from validateit.exc import ValidationError

        ..  doctest:: add_context

            >>> e = ValidationError()
            >>> e
            <ValidationError()>
            >>> e.context
            []

            >>> e.add_context("foo")
            <foo: ValidationError()>
            >>> e.context
            ['foo']

            >>> e.add_context("x.y")
            <[x.y].foo: ValidationError()>
            >>> e.context
            ['x.y', 'foo']

            >>> e.add_context(1)
            <1.[x.y].foo: ValidationError()>
            >>> e.context
            [1, 'x.y', 'foo']

        """
        self.context.insert(0, node)
        return self

    def __iter__(self):
        yield self

    def __repr__(self):
        if self.context:
            return "<%s: %s>" % (self._repr_context(), self._repr_error())
        else:
            return "<%s>" % self._repr_error()

    def __str__(self):
        return repr(self)

    def _repr_context(self):
        def context():
            for node in self.context:
                if isinstance(node, str) and "." in node:
                    yield "[%s]" % node
                else:
                    yield str(node)

        return ".".join(context())

    def _repr_error(self):
        def params():
            for slot in self.__slots__[1:]:  # Exclude ``context``
                yield "%s=%r" % (slot, getattr(self, slot))

        return "%s(%s)" % (self.__class__.__name__, ", ".join(params()))


class ConditionError(ValidationError):
    """Base Class for Condition Errors"""

    __slots__ = ValidationError.__slots__ + ("expected", "actual")


class InvalidTypeError(ConditionError):
    """
    Invalid Type Error

    :param type expected:
        expected type or types.
    :type expected: type or tuple

    :param type actual:
        actual type.

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
        * ``number`` on test for ``Not-a-Number``;
        * ``finite`` on test for ``Infinity``.

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
        actual value.

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
        pattern.

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
    """Base Class for Mapping Key Errors"""

    __slots__ = ValidationError.__slots__

    def __init__(self, key, **kw):
        super(MappingKeyError, self).__init__(context=[key], **kw)


class ForbiddenKeyError(MappingKeyError):
    """Forbidden Mapping Key Error"""

    __slots__ = MappingKeyError.__slots__


class MissingKeyError(MappingKeyError):
    """Missing Mapping Key Error"""

    __slots__ = MappingKeyError.__slots__


class ExtraKeyError(MappingKeyError):
    """
    Extra Mapping Key Error

    :param ValidationError key_error:
        error occurred during extra key validation.

    :param ValidationError value_error:
        error occurred during extra value validation.

    """

    __slots__ = MappingKeyError.__slots__ + ("key_error", "value_error")


class SchemaError(ValidationError):
    """
    Schema Error

    :param list errors:
        list of all errors occurred during complex structure validation.

    """

    __slots__ = ValidationError.__slots__ + ("errors",)

    def __init__(self, errors):
        super(SchemaError, self).__init__(errors=errors)

    def __iter__(self):
        return (e for e in self.errors)

    def __repr__(self):
        errors = ",\n".join("    %r" % e for e in self.errors)
        return "<%s(errors=[\n%s\n])>" % (self.__class__.__name__, errors)

    def add_context(self, node):
        for e in self.errors:
            e.add_context(node)
        return self


class StepNo(object):
    """
    Step Number Context Marker

    It is a special context marker,
    that is used by pipeline validators to indicate,
    which validation step is failed.

    :param int no:
        number of step.

    ..  testsetup:: stepno

        from validateit import AnyOf, Int
        from validateit.exc import ValidationError

    ..  doctest:: stepno

        >>> schema = AnyOf(Int(min=0, max=10), Int(min=90, max=100))
        >>> try:
        ...     schema(50)
        ... except ValidationError as e:
        ...     error = e

        >>> error
        <SchemaError(errors=[
            <<StepNo(0)>: MaxValueError(expected=10, actual=50)>,
            <<StepNo(1)>: MinValueError(expected=90, actual=50)>
        ])>

        >>> error.errors[0].context[0]
        <StepNo(0)>

        >>> error.errors[0].context[0].no
        0

    """

    __slots__ = ("no",)

    def __init__(self, no):
        self.no = no

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, self.no)

    def __eq__(self, other):
        return self.__class__ is type(other) and self.no == other.no
