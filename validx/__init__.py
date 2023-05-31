from . import exc

try:
    from .cy import (
        __impl__,
        Validator,
        Int,
        Float,
        Decimal,
        Str,
        Bytes,
        Date,
        Time,
        Datetime,
        Bool,
        List,
        Set,
        Tuple,
        Dict,
        AllOf,
        OneOf,
        LazyRef,
        Type,
        Const,
        Any,
        classes,
        instances,
    )
except ImportError:  # pragma: no cover
    from .py import (  # type: ignore
        __impl__,
        Validator,
        Int,
        Float,
        Decimal,
        Str,
        Bytes,
        Date,
        Time,
        Datetime,
        Bool,
        List,
        Set,
        Tuple,
        Dict,
        AllOf,
        OneOf,
        LazyRef,
        Type,
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
    "Decimal",
    "Str",
    "Bytes",
    "Date",
    "Time",
    "Datetime",
    "Bool",
    "List",
    "Set",
    "Tuple",
    "Dict",
    "AllOf",
    "OneOf",
    "LazyRef",
    "Type",
    "Const",
    "Any",
    "classes",
    "instances",
]

__impl__ = __impl__
__version__ = "0.8"
__author__ = "Cottonwood Technology <info@cottonwood.tech>"
__license__ = "BSD"
