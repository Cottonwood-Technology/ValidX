class ValidationError(ValueError):

    __slots__ = ("context",)

    def __init__(self, **kw):
        kw.setdefault("context", [])
        for slot, value in kw.items():
            setattr(self, slot, value)
        super(ValidationError, self).__init__(
            *(getattr(self, slot) for slot in self.__slots__)
        )

    def add_context(self, node):
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
    __slots__ = ValidationError.__slots__ + ("expected", "actual")


class InvalidTypeError(ConditionError):
    __slots__ = ConditionError.__slots__


class OptionsError(ConditionError):
    __slots__ = ConditionError.__slots__


class MinValueError(ConditionError):
    __slots__ = ConditionError.__slots__


class MaxValueError(ConditionError):
    __slots__ = ConditionError.__slots__


class FloatValueError(ConditionError):
    __slots__ = ConditionError.__slots__


class StrDecodeError(ConditionError):
    __slots__ = ConditionError.__slots__


class MinLengthError(ConditionError):
    __slots__ = ConditionError.__slots__


class MaxLengthError(ConditionError):
    __slots__ = ConditionError.__slots__


class TupleLengthError(ConditionError):
    __slots__ = ConditionError.__slots__


class PatternMatchError(ConditionError):
    __slots__ = ConditionError.__slots__


class MappingKeyError(ValidationError):
    __slots__ = ValidationError.__slots__

    def __init__(self, key):
        super(MappingKeyError, self).__init__(context=[key])


class ForbiddenKeyError(MappingKeyError):
    __slots__ = MappingKeyError.__slots__


class MissingKeyError(MappingKeyError):
    __slots__ = MappingKeyError.__slots__


class SchemaError(ValidationError):
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
