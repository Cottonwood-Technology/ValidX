import typing as t


class ValidationError(ValueError):
    pass


class ConditionError(ValidationError):

    expected: t.Any
    actual: t.Any

    def __init__(self, expected: t.Any, actual: t.Any) -> None:
        ...


class InvalidTypeError(ConditionError):
    pass


class OptionsError(ConditionError):
    pass


class MinValueError(ConditionError):
    pass


class MaxValueError(ConditionError):
    pass


class FloatValueError(ConditionError):
    pass


class StrDecodeError(ConditionError):
    pass


class MinLengthError(ConditionError):
    pass


class MaxLengthError(ConditionError):
    pass


class TupleLengthError(ConditionError):
    pass


class PatternMatchError(ConditionError):
    pass


class SchemaError(ValidationError):

    errors: t.List[t.Tuple[t.Any, ValidationError]]

    def __init__(self, errors: t.List[t.Tuple[t.Any, ValidationError]]) -> None:
        ...


class MappingKeyError(ValidationError):

    key: t.List[t.Tuple[t.Any, ValidationError]]

    def __init__(self, key: t.Any) -> None:
        ...


class ExtraKeyError(MappingKeyError):
    pass


class RequiredKeyError(MappingKeyError):
    pass
