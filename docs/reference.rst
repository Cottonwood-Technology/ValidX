.. _reference:

Reference
=========

Abstract
--------

..  autoclass:: validateit.py.Validator

    ..  automethod:: __call__
    ..  automethod:: load
    ..  automethod:: dump
    ..  automethod:: clone


Numbers
-------

..  autoclass:: validateit.py.Int
..  autoclass:: validateit.py.Float


Chars
-----

..  autoclass:: validateit.py.Str
..  autoclass:: validateit.py.Bytes


Date and Time
-------------

..  autoclass:: validateit.py.Date
..  autoclass:: validateit.py.Time
..  autoclass:: validateit.py.Datetime


Boolean
-------

..  autoclass:: validateit.py.Bool


Sequences
---------

..  autoclass:: validateit.py.List
..  autoclass:: validateit.py.Sequence
..  autoclass:: validateit.py.Tuple


Mappings
--------

..  autoclass:: validateit.py.Dict
..  autoclass:: validateit.py.Mapping


Pipelines
---------

..  autoclass:: validateit.py.AllOf
..  autoclass:: validateit.py.OneOf


Special
-------

..  autoclass:: validateit.py.LazyRef
..  autoclass:: validateit.py.Const
..  autoclass:: validateit.py.Any


Registries
----------

..  automodule:: validateit.py.classes

    ..  autofunction:: add
    ..  autofunction:: get


..  automodule:: validateit.py.instances

    ..  autofunction:: add
    ..  autofunction:: put
    ..  autofunction:: get
    ..  autofunction:: clear


Errors
------

..  py:currentmodule:: validateit.exc

The class hierarchy for exceptions is:

*   ``ValueError`` (built-in)

    *   :class:`ValidationError`

        *   :class:`ConditionError`

            *   :class:`InvalidTypeError`
            *   :class:`OptionsError`
            *   :class:`MinValueError`
            *   :class:`MaxValueError`
            *   :class:`FloatValueError`
            *   :class:`StrDecodeError`
            *   :class:`MinLengthError`
            *   :class:`MaxLengthError`
            *   :class:`TupleLengthError`
            *   :class:`PatternMatchError`
            *   :class:`DatetimeParseError`
            *   :class:`RecursionMaxDepthError`

        *   :class:`MappingKeyError`

            *   :class:`ForbiddenKeyError`
            *   :class:`MissingKeyError`

        *   :class:`SchemaError`


..  autoclass:: validateit.exc.ValidationError

    .. automethod:: add_context

..  autoclass:: validateit.exc.ConditionError
..  autoclass:: validateit.exc.InvalidTypeError
..  autoclass:: validateit.exc.OptionsError
..  autoclass:: validateit.exc.MinValueError
..  autoclass:: validateit.exc.MaxValueError
..  autoclass:: validateit.exc.FloatValueError
..  autoclass:: validateit.exc.StrDecodeError
..  autoclass:: validateit.exc.MinLengthError
..  autoclass:: validateit.exc.MaxLengthError
..  autoclass:: validateit.exc.TupleLengthError
..  autoclass:: validateit.exc.PatternMatchError
..  autoclass:: validateit.exc.DatetimeParseError
..  autoclass:: validateit.exc.RecursionMaxDepthError
..  autoclass:: validateit.exc.MappingKeyError
..  autoclass:: validateit.exc.ForbiddenKeyError
..  autoclass:: validateit.exc.MissingKeyError
..  autoclass:: validateit.exc.SchemaError


Context Markers
---------------

..  autoclass:: validateit.exc.Extra
..  autoclass:: validateit.exc.Step


Error Formatter
---------------

..  autoclass:: validateit.exc.Formatter

    ..  automethod:: __call__
