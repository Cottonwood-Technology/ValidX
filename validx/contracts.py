from .compat.colabc import Container, Sequence, Mapping, Callable
from .compat.immutables import Map
from .compat.types import chars, basestr


def expect(
    obj, attr, value, nullable=False, types=None, not_types=None, convert_to=None
):
    if nullable and value is None:
        return value
    if types is not None and not isinstance(value, types):
        raise TypeError(
            "%s.%s.%s should be of type %r"
            % (obj.__class__.__module__, obj.__class__.__name__, attr, types)
        )
    if not_types is not None and isinstance(value, not_types):
        raise TypeError(
            "%s.%s.%s should not be of type %r"
            % (obj.__class__.__module__, obj.__class__.__name__, attr, not_types)
        )
    if convert_to is not None and not isinstance(value, convert_to):
        value = convert_to(value)
    return value


def expect_flag(obj, attr, value):
    return expect(obj, attr, value, types=(bool, int, type(None)), convert_to=bool)


def expect_length(obj, attr, value, nullable=False):
    value = expect(obj, attr, value, nullable=nullable, types=int)
    if value is not None:
        if value < 0:
            raise ValueError(
                "%s.%s.%s should not be negative number"
                % (obj.__class__.__module__, obj.__class__.__name__, attr)
            )
    return value


def expect_basestr(obj, attr, value, nullable=False):
    return expect(obj, attr, value, nullable=nullable, types=basestr)


def expect_callable(obj, attr, value, nullable=False):
    return expect(obj, attr, value, nullable=nullable, types=Callable)


def expect_container(obj, attr, value, nullable=False, empty=False, item_type=None):
    value = expect(
        obj, attr, value, nullable=nullable, types=Container, not_types=chars
    )
    if value is not None:
        if not isinstance(value, frozenset):
            try:
                value = frozenset(value)
            except TypeError:
                # Unhashable type, fallback to tuple
                value = tuple(value)
        if not value and not empty:
            raise ValueError(
                "%s.%s.%s should not be empty"
                % (obj.__class__.__module__, obj.__class__.__name__, attr)
            )
        if item_type is not None:
            for item in value:
                if not isinstance(item, item_type):
                    raise TypeError(
                        "%s.%s.%s items should be of type %r, got %r"
                        % (
                            obj.__class__.__module__,
                            obj.__class__.__name__,
                            attr,
                            item_type,
                            type(item),
                        )
                    )
    return value


def expect_sequence(obj, attr, value, nullable=False, empty=False, item_type=None):
    value = expect(
        obj,
        attr,
        value,
        nullable=nullable,
        types=Sequence,
        not_types=chars,
        convert_to=tuple,
    )
    if value is not None:
        if not value and not empty:
            raise ValueError(
                "%s.%s.%s should not be empty"
                % (obj.__class__.__module__, obj.__class__.__name__, attr)
            )
        if item_type is not None:
            for n, item in enumerate(value):
                if not isinstance(item, item_type):
                    raise TypeError(
                        "%s.%s.%s[%s] value should be of type %r"
                        % (
                            obj.__class__.__module__,
                            obj.__class__.__name__,
                            attr,
                            n,
                            item_type,
                        )
                    )
    return value


def expect_mapping(obj, attr, value, nullable=False, empty=False, value_type=None):
    value = expect(obj, attr, value, nullable=nullable, types=Mapping, convert_to=Map)
    if value is not None:
        if not value and not empty:
            raise ValueError(
                "%s.%s.%s should not be empty"
                % (obj.__class__.__module__, obj.__class__.__name__, attr)
            )
        if value_type is not None:
            for key, val in value.items():
                if not isinstance(val, value_type):
                    raise TypeError(
                        "%s.%s.%s[%r] value should be of type %r"
                        % (
                            obj.__class__.__module__,
                            obj.__class__.__name__,
                            attr,
                            key,
                            value_type,
                        )
                    )
    return value


def expect_tuple(obj, attr, value, struct, nullable=False):
    value = expect(
        obj,
        attr,
        value,
        nullable=nullable,
        types=Sequence,
        not_types=chars,
        convert_to=tuple,
    )
    if value is not None:
        if len(value) != len(struct):
            raise ValueError(
                "%s.%s.%s should be a tuple of %r"
                % (obj.__class__.__module__, obj.__class__.__name__, attr, struct)
            )
        for n, (item_type, item) in enumerate(zip(struct, value)):
            if not isinstance(item, item_type):
                raise TypeError(
                    "%s.%s.%s[%s] value should be of type %r"
                    % (
                        obj.__class__.__module__,
                        obj.__class__.__name__,
                        attr,
                        n,
                        item_type,
                    )
                )
    return value
