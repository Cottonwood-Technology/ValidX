Changes
=======

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
