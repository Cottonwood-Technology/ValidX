Changes
=======


0.8.dev0
--------

*   Dropped Python 3.5 support.
*   Added Python 3.10, 3.11 support.
*   Fixed handling UNIX-timestamps by ``Date`` and ``Datetime`` validators.
*   Added ability to specify default time which is used to implicitly convert
    ``date`` to ``datetime`` within ``Datetime`` validator.
*   Fixed handling ``bool`` values by ``Int`` and ``Float`` validators.
*   Changed behavior of ``Str`` validator,
    it now strips leading & trailing whitespace by default.
    Use ``dontstrip=True`` parameter to disable the stripping.
*   Added ability to normalize spaces by ``Str`` validator,
    i.e. replace space sequences by single space character.
    Use ``normspace=True`` parameter to enable the normalization.
*   Unified behavior of Python and Cython versions of ``Int`` validator.
    Both versions support unlimited integer numbers now.
*   Added new ``Set`` validator.
*   Added new ``Decimal`` validator.
*   Renamed ``FloatValueError`` to ``NumberError``,
    so it is now used for both ``Float`` and ``Decimal`` validators.
*   Added new ``CoerceError`` which is raised 
    instead of ``InvalidTypeError`` when type coercion fails.


0.7
---

*   Dropped Python 2.7 support.
*   Fixed ``relmin/relmax`` checks for ``Date`` validator with timezone.
*   Fixed constructing Cython version of ``Type`` validator with type created from metaclass.


0.6.1
-----

*   Fixed type declarations for ``Validator.clone()`` method.


0.6
---

*   Added Python 3.8 into test matrix.
*   Made validators immutable.
*   Added contracts checks on validator initialization.
*   Added new simplified syntax for cloning validators.
*   Got rid of global state within ``LazyRef`` validator.
    It now acts like a pure function.
*   Fixed raising of ambiguous ``MinLengthError`` on ``List`` and ``Dict`` validation.



0.5.1
-----

*   Fixed type declarations. Again. One does not simply make mypy happy.


0.5
---

*   Removed confusing nullable check from ``Any`` validator.
*   Fixed type declarations.


0.4
---

*   Fixed library objects pickling.
*   Fixed checking of length within ``List`` validator.


0.3
---

*   Fixed handling of default values and length validation within ``Dict`` validator.


0.2
---

*   Added support of timezones into ``Date`` and ``Datetime`` validators.
*   Added support of custom parsers into ``Date``, ``Time``, and ``Datetime`` validators.
*   Added ``Type`` validator for custom types.


0.1
---

*   Initial release.
