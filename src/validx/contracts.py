from collections.abc import Container, Sequence, Mapping, Callable

from .types import chars, frozendict


def expect(
    obj, attr, value, nullable=False, types=None, not_types=None, convert_to=None
):
    """
    Check, whether the value satisfies expectations

    :param obj:
        an object,
        which will set the value to its attribute.
        It is used to make error messages more specific.

    :param str attr:
        name of an attribute of the object.
        It is used to make error messages more specific.

    :param value:
        checked value itself.

    :param bool nullable:
        accept ``None`` as a valid value.
        Default: ``False`` — does not accept ``None``.

    :param types:
        define acceptable types of the value.
        Default: ``None`` — accept any type.
    :type types: None, type or tuple

    :param not_types:
        define implicitly unacceptable types of the value.
        Default: ``None`` — accept any type.
    :type types: None, type or tuple

    :param type convert_to:
        convert the value to specified type.
        Default: ``None`` — does not convert the value.

    :raises TypeError:
        * if ``types is not None`` and ``not isinstance(value, types)``;
        * if ``not_types is not None`` and ``isinstance(value, not_types)``.

    """
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
    """
    Check, whether the value satisfies expectations of boolean flag

    :param obj:
        an object,
        which will set the value to its attribute.
        It is used to make error messages more specific.

    :param str attr:
        name of an attribute of the object.
        It is used to make error messages more specific.

    :param value:
        checked value itself.

    :param bool nullable:
        accept ``None`` as a valid value.
        Default: ``False`` — does not accept ``None``.

    :raises TypeError:
        if ``not isinstance(value, (bool, int, type(None)))``.

    """
    return expect(obj, attr, value, types=(bool, int, type(None)), convert_to=bool)


def expect_length(obj, attr, value, nullable=False):
    """
    Check, whether the value satisfies expectations of integer length

    :param obj:
        an object,
        which will set the value to its attribute.
        It is used to make error messages more specific.

    :param str attr:
        name of an attribute of the object.
        It is used to make error messages more specific.

    :param value:
        checked value itself.

    :param bool nullable:
        accept ``None`` as a valid value.
        Default: ``False`` — does not accept ``None``.

    :raises TypeError:
        if ``not isinstance(value, int)``.

    :raises ValueError:
        if ``value < 0``.

    """
    value = expect(obj, attr, value, nullable=nullable, types=int)
    if value is not None:
        if value < 0:
            raise ValueError(
                "%s.%s.%s should not be negative number"
                % (obj.__class__.__module__, obj.__class__.__name__, attr)
            )
    return value


def expect_str(obj, attr, value, nullable=False):
    """
    Check, whether the value satisfies expectations of base string

    :param obj:
        an object,
        which will set the value to its attribute.
        It is used to make error messages more specific.

    :param str attr:
        name of an attribute of the object.
        It is used to make error messages more specific.

    :param value:
        checked value itself.

    :param bool nullable:
        accept ``None`` as a valid value.
        Default: ``False`` — does not accept ``None``.

    :raises TypeError:
        if ``not isinstance(value, str)``.

    """
    return expect(obj, attr, value, nullable=nullable, types=str)


def expect_callable(obj, attr, value, nullable=False):
    """
    Check, whether the value satisfies expectations of callable

    :param obj:
        an object,
        which will set the value to its attribute.
        It is used to make error messages more specific.

    :param str attr:
        name of an attribute of the object.
        It is used to make error messages more specific.

    :param value:
        checked value itself.

    :param bool nullable:
        accept ``None`` as a valid value.
        Default: ``False`` — does not accept ``None``.

    :raises TypeError:
        if ``not isinstance(value, collections.abc.Callable)``.

    """
    return expect(obj, attr, value, nullable=nullable, types=Callable)


def expect_container(obj, attr, value, nullable=False, empty=False, item_type=None):
    """
    Check, whether the value satisfies expectations of container

    :param obj:
        an object,
        which will set the value to its attribute.
        It is used to make error messages more specific.

    :param str attr:
        name of an attribute of the object.
        It is used to make error messages more specific.

    :param value:
        checked value itself.

    :param bool nullable:
        accept ``None`` as a valid value.
        Default: ``False`` — does not accept ``None``.

    :param bool empty:
        accept empty container as a valid value.
        Default: ``False`` — does not accept empty container.

    :param type item_type:
        check,
        whether each item of the container has specified type.
        Default: ``None`` — does not check items.

    :raises TypeError:
        * if ``not isinstance(value, collections.abc.Container)``;
        * if ``isinstance(value, (str, bytes))``;
        * if ``item_type is not None`` and ``isinstance(item, item_type)``,
          ``for item in value``.

    :raises ValueError:
        if ``not empty`` and ``not value``.

    :returns:
        passed container converted to ``frozenset``,
        if items are hashable,
        otherwise to ``tuple``.

    """
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
    """
    Check, whether the value satisfies expectations of sequence

    :param obj:
        an object,
        which will set the value to its attribute.
        It is used to make error messages more specific.

    :param str attr:
        name of an attribute of the object.
        It is used to make error messages more specific.

    :param value:
        checked value itself.

    :param bool nullable:
        accept ``None`` as a valid value.
        Default: ``False`` — does not accept ``None``.

    :param bool empty:
        accept empty sequence as a valid value.
        Default: ``False`` — does not accept empty sequence.

    :param type item_type:
        check,
        whether each item of the sequence has specified type.
        Default: ``None`` — does not check items.

    :raises TypeError:
        * if ``not isinstance(value, collections.abc.Sequence)``;
        * if ``isinstance(value, (str, bytes))``;
        * if ``item_type is not None`` and ``isinstance(item, item_type)``,
          ``for item in value``.

    :raises ValueError:
        if ``not empty`` and ``not value``.

    :returns:
        passed sequence converted to ``tuple``.

    """
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
    """
    Check, whether the value satisfies expectations of mapping

    :param obj:
        an object,
        which will set the value to its attribute.
        It is used to make error messages more specific.

    :param str attr:
        name of an attribute of the object.
        It is used to make error messages more specific.

    :param value:
        checked value itself.

    :param bool nullable:
        accept ``None`` as a valid value.
        Default: ``False`` — does not accept ``None``.

    :param bool empty:
        accept empty mapping as a valid value.
        Default: ``False`` — does not accept empty mapping.

    :param type value_type:
        check,
        whether each value of the mapping has specified type.
        Default: ``None`` — does not check items.

    :raises TypeError:
        * if ``not isinstance(value, collections.abc.Sequence)``;
        * if ``isinstance(value, (str, bytes))``;
        * if ``value_type is not None`` and ``isinstance(val, value_type)``,
          ``for key, val in value.items()``.

    :raises ValueError:
        if ``not empty`` and ``not value``.

    :returns:
        passed mapping converted to ``frozendict``.

    """
    value = expect(
        obj, attr, value, nullable=nullable, types=Mapping, convert_to=frozendict
    )
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
    """
    Check, whether the value satisfies expectations of tuple of specific structure

    :param obj:
        an object,
        which will set the value to its attribute.
        It is used to make error messages more specific.

    :param str attr:
        name of an attribute of the object.
        It is used to make error messages more specific.

    :param value:
        checked value itself.

    :param tuple struct:
        tuple of types.

    :param bool nullable:
        accept ``None`` as a valid value.
        Default: ``False`` — does not accept ``None``.

    :raises TypeError:
        * if ``not isinstance(value, collections.abc.Sequence)``;
        * if ``isinstance(value, (str, bytes))``;
        * if ``not isinstance(item, item_type)``,
          ``for item_type, item in zip(struct, value)``.

    :raises ValueError:
        if ``len(value) != len(struct)``.

    :returns:
        passed sequence converted to ``tuple``.

    """
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
