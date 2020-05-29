Changes
=======

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

*   Added support of timezones into :class:`validx.py.Date` and :class:`validx.py.Datetime` validators.
*   Added support of custom parsers into :class:`validx.py.Date`,
    :class:`validx.py.Time`,
    and :class:`validx.py.Datetime` validators.
*   Added :class:`validx.py.Type` validator for custom types.


0.1
---

*   Initial release.
