import typing as t

class ValidationError(ValueError):
    __slots__: t.Tuple[str, ...]
    args: t.Tuple[t.Any, t.Any]
    context: t.Deque
    def __init__(self, *, context: t.Deque = None, **kw) -> None: ...
    def add_context(self, node: t.Any) -> ValidationError: ...
    def __iter__(self) -> t.Iterator[ValidationError]: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def _repr_context(self) -> str: ...
    def _repr_error(self) -> str: ...

class ConditionError(ValidationError):
    __slots__: t.Tuple[str, ...]
    expected: t.Any
    actual: t.Any
    def __init__(
        self, *, context: t.Deque = None, expected: t.Any, actual: t.Any
    ) -> None: ...

class InvalidTypeError(ConditionError):
    __slots__: t.Tuple[str, ...]

class OptionsError(ConditionError):
    __slots__: t.Tuple[str, ...]

class MinValueError(ConditionError):
    __slots__: t.Tuple[str, ...]

class MaxValueError(ConditionError):
    __slots__: t.Tuple[str, ...]

class FloatValueError(ConditionError):
    __slots__: t.Tuple[str, ...]

class StrDecodeError(ConditionError):
    __slots__: t.Tuple[str, ...]

class MinLengthError(ConditionError):
    __slots__: t.Tuple[str, ...]

class MaxLengthError(ConditionError):
    __slots__: t.Tuple[str, ...]

class TupleLengthError(ConditionError):
    __slots__: t.Tuple[str, ...]

class PatternMatchError(ConditionError):
    __slots__: t.Tuple[str, ...]

class DatetimeParseError(ConditionError):
    __slots__: t.Tuple[str, ...]

class RecursionMaxDepthError(ConditionError):
    __slots__: t.Tuple[str, ...]

class MappingKeyError(ValidationError):
    __slots__: t.Tuple[str, ...]
    def __init__(self, key: t.Any, **kw) -> None: ...

class ForbiddenKeyError(MappingKeyError):
    __slots__: t.Tuple[str, ...]

class MissingKeyError(MappingKeyError):
    __slots__: t.Tuple[str, ...]

class ExtraKeyError(MappingKeyError):
    __slots__: t.Tuple[str, ...]
    key_error: t.Optional[ValidationError]
    value_error: t.Optional[ValidationError]
    def __init__(
        self,
        key: t.Any,
        *,
        key_error: ValidationError = None,
        value_error: ValidationError = None,
    ) -> None: ...

class SchemaError(ValidationError):
    __slots__: t.Tuple[str, ...]
    errors: t.List[ValidationError]
    def __init__(self, errors: t.List[ValidationError]) -> None: ...

class Step(object):
    __slots__: t.Tuple[str, ...]
    num: int
    def __init__(self, num: int) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: t.Any) -> bool: ...
