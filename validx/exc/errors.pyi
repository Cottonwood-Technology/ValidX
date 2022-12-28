from collections.abc import Sequence
import typing as t

class ValidationError(ValueError, Sequence):
    __slots__: t.Tuple[str, ...]
    args: t.Tuple[t.Any, t.Any]
    context: t.Deque
    def __init__(self, *, context: t.Deque = None, **kw) -> None: ...
    def add_context(self, node: t.Any) -> ValidationError: ...
    def __getitem__(self, index: t.Union[int, slice]) -> ValidationError: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> t.Iterator[ValidationError]: ...
    def sort(self, key: t.Callable = None, reverse: bool = False) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def format_context(self) -> str: ...
    def format_error(self) -> str: ...

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

class DatetimeTypeError(ConditionError):
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

class SchemaError(ValidationError):
    __slots__: t.Tuple[str, ...]
    errors: t.List[ValidationError]
    def __init__(self, errors: t.List[ValidationError]) -> None: ...
