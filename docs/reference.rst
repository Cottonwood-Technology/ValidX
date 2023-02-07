.. _reference:

Reference
=========

Abstract
--------

..  autoclass:: validx.py.Validator

    ..  automethod:: __call__
    ..  automethod:: load
    ..  automethod:: dump
    ..  automethod:: clone


Numbers
-------

..  autoclass:: validx.py.Int
..  autoclass:: validx.py.Float
..  autoclass:: validx.py.Decimal


Chars
-----

..  autoclass:: validx.py.Str
..  autoclass:: validx.py.Bytes


Date and Time
-------------

..  autoclass:: validx.py.Date
..  autoclass:: validx.py.Time
..  autoclass:: validx.py.Datetime


Boolean
-------

..  autoclass:: validx.py.Bool


Containers
----------

..  autoclass:: validx.py.List
..  autoclass:: validx.py.Set
..  autoclass:: validx.py.Tuple
..  autoclass:: validx.py.Dict


Pipelines
---------

..  autoclass:: validx.py.AllOf
..  autoclass:: validx.py.OneOf


Special
-------

..  autoclass:: validx.py.LazyRef
..  autoclass:: validx.py.Type
..  autoclass:: validx.py.Const
..  autoclass:: validx.py.Any


Class Registry
--------------

..  autofunction:: validx.py.classes.add
..  autofunction:: validx.py.classes.get


.. _reference-instance-registry:

Instance Registry
-----------------

..  autofunction:: validx.py.instances.add
..  autofunction:: validx.py.instances.put
..  autofunction:: validx.py.instances.get
..  autofunction:: validx.py.instances.clear


Errors
------

..  py:currentmodule:: validx.exc

The class hierarchy for exceptions is:

*   ``ValueError`` (built-in)

    *   :class:`ValidationError`

        *   :class:`ConditionError`

            *   :class:`InvalidTypeError`
            *   :class:`OptionsError`
            *   :class:`MinValueError`
            *   :class:`MaxValueError`
            *   :class:`NumberError`
            *   :class:`StrDecodeError`
            *   :class:`MinLengthError`
            *   :class:`MaxLengthError`
            *   :class:`TupleLengthError`
            *   :class:`PatternMatchError`
            *   :class:`DatetimeParseError`
            *   :class:`DatetimeTypeError`
            *   :class:`RecursionMaxDepthError`

        *   :class:`MappingKeyError`

            *   :class:`ForbiddenKeyError`
            *   :class:`MissingKeyError`

        *   :class:`SchemaError`


..  autoclass:: validx.exc.ValidationError

    .. automethod:: add_context

..  autoclass:: validx.exc.ConditionError
..  autoclass:: validx.exc.InvalidTypeError
..  autoclass:: validx.exc.OptionsError
..  autoclass:: validx.exc.MinValueError
..  autoclass:: validx.exc.MaxValueError
..  autoclass:: validx.exc.NumberError
..  autoclass:: validx.exc.StrDecodeError
..  autoclass:: validx.exc.MinLengthError
..  autoclass:: validx.exc.MaxLengthError
..  autoclass:: validx.exc.TupleLengthError
..  autoclass:: validx.exc.PatternMatchError
..  autoclass:: validx.exc.DatetimeParseError
..  autoclass:: validx.exc.DatetimeTypeError
..  autoclass:: validx.exc.RecursionMaxDepthError
..  autoclass:: validx.exc.MappingKeyError
..  autoclass:: validx.exc.ForbiddenKeyError
..  autoclass:: validx.exc.MissingKeyError
..  autoclass:: validx.exc.SchemaError


.. _reference-context-markers:

Context Markers
---------------

..  autoclass:: validx.exc.Extra
..  autoclass:: validx.exc.Step


.. _reference-error-formatter:

Error Formatter
---------------

..  autoclass:: validx.exc.Formatter

    ..  automethod:: __call__
