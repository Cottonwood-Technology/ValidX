from . import exc

try:
    from .cy import (
        __impl__,
        Validator,
        Int,
        Float,
        Str,
        Bytes,
        Date,
        Time,
        Datetime,
        Bool,
        List,
        Tuple,
        Dict,
        AllOf,
        OneOf,
        LazyRef,
        Const,
        Any,
        classes,
        instances,
    )
except ImportError:  # pragma: no cover
    from .py import (
        __impl__,
        Validator,
        Int,
        Float,
        Str,
        Bytes,
        Date,
        Time,
        Datetime,
        Bool,
        List,
        Tuple,
        Dict,
        AllOf,
        OneOf,
        LazyRef,
        Const,
        Any,
        classes,
        instances,
    )


__all__ = [
    "exc",
    "Validator",
    "Int",
    "Float",
    "Str",
    "Bytes",
    "Date",
    "Time",
    "Datetime",
    "Bool",
    "List",
    "Tuple",
    "Dict",
    "AllOf",
    "OneOf",
    "LazyRef",
    "Const",
    "Any",
    "classes",
    "instances",
]

__impl__ = __impl__
__version__ = "0.1"
__author__ = "Cottonwood Technology <info@cottonwood.tech>"
__license__ = "BSD"
