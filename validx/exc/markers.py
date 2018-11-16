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

        >>> from validx import exc, Dict, Str

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

        >>> repr(error[0].context[1])
        '@KEY'
        >>> error[0].context[1].name
        'KEY'

        >>> error[0].context[1] is exc.EXTRA_KEY
        True
        >>> error[1].context[1] is exc.EXTRA_VALUE
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

        >>> from validx import exc, OneOf, Int

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

        >>> repr(error[0].context[0])
        '#0'
        >>> error[0].context[0].num
        0
        >>> isinstance(error[0].context[0], exc.Step)
        True

    """

    __slots__ = ("num",)

    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return "#%s" % self.num

    def __eq__(self, other):
        return self.__class__ is type(other) and self.num == other.num
