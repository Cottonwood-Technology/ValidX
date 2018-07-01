class ValidationError(ValueError):
    pass


class ConditionError(ValidationError):
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual
        super(ConditionError, self).__init__(self.expected, self.actual)


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
    def __init__(self, errors):
        self.errors = errors
        super(SchemaError, self).__init__(self.errors)


class MappingKeyError(ValidationError):
    def __init__(self, key):
        self.key = key
        super(MappingKeyError, self).__init__(self.key)


class ExtraKeyError(MappingKeyError):
    pass


class RequiredKeyError(MappingKeyError):
    pass
