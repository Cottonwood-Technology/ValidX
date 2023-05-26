Changes
=======

0.8.dev0
--------

*   Dropped Python 3.5 support.
*   Added Python 3.10, 3.11 support.
*   Fixed handling UNIX-timestamps by :class:`validx.py.Date`
    and :class:`validx.py.Datetime` validators.
*   Fixed handling ``bool`` values by :class:`validx.py.Int`
    and :class:`validx.py.Float` validators.
*   Changed behavior of :class:`validx.py.Str` validator,
    it now strips leading & trailing whitespace by default.
    Use ``dontstrip=True`` parameter to disable the stripping.
*   Added ability to normalize spaces by :class:`validx.py.Str` validator,
    i.e. replace space sequences by single space character.
    Use ``normspace=True`` parameter to enable the normalization.
*   Unified behavior of Python and Cython versions of :class:`validx.py.Int` validator.
    Both versions support unlimited integer numbers now.
*   Added new :class:`validx.py.Set` validator.
*   Added new :class:`validx.py.Decimal` validator.
*   Renamed ``FloatValueError`` to :class:`validx.exc.NumberError`,
    so it is now used for both :class:`validx.py.Float`
    and :class:`validx.py.Decimal` validators.
*   Added new :class:`validx.exc.CoerceError` which is raised 
    instead of :class:`validx.exc.InvalidTypeError` when type coercion fails.    


0.7
---

*   Dropped Python 2.7 support.
*   Fixed ``relmin/relmax`` checks for :class:`validx.py.Date` validator with timezone.
*   Fixed constructing Cython version of :class:`validx.py.Type` validator
    with type created from metaclass.


0.6.1
-----

*   Fixed type declarations for :meth:`validx.py.Validator.clone` method.


0.6
---

*   Added Python 3.8 into test matrix.
*   Made validators immutable.
*   Added contracts checks on validator initialization.
*   Added new simplified syntax for :ref:`usage-cloning-validators`.
*   Got rid of global state within :class:`validx.py.LazyRef` validator.
    It now acts like a pure function.
*   Fixed raising of ambiguous :class:`validx.exc.MinLengthError` on
    :class:`validx.py.List` and :class:`validx.py.Dict` validation.


0.5.1
-----

*   Fixed type declarations. Again. One does not simply make mypy happy.


0.5
---

*   Removed confusing nullable check from :class:`validx.py.Any` validator.
*   Fixed type declarations.


0.4
---

*   Fixed library objects pickling.
*   Fixed checking of length within :class:`validx.py.List` validator.


0.3
---

*   Fixed handling of default values and length validation within :class:`validx.py.Dict` validator.


0.2
---

*   Added support of timezones into :class:`validx.py.Date`
    and :class:`validx.py.Datetime` validators.
*   Added support of custom parsers into :class:`validx.py.Date`,
    :class:`validx.py.Time`,
    and :class:`validx.py.Datetime` validators.
*   Added :class:`validx.py.Type` validator for custom types.


0.1
---

*   Initial release.
