import typing as t
from . import abstract


class Int(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    coerce: t.Optional[bool]
    min: t.Optional[int]
    max: t.Optional[int]
    options: t.Optional[t.Container[int]]

    def __init__(
        self,
        *,
        nullable: t.Optional[bool] = None,
        coerce: t.Optional[bool] = None,
        min: t.Optional[int] = None,
        max: t.Optional[int] = None,
        options: t.Optional[t.Container[int]] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...


class Float(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    coerce: t.Optional[bool]
    nan: t.Optional[bool]
    inf: t.Optional[bool]
    min: t.Optional[float]
    max: t.Optional[float]

    def __init__(
        self,
        *,
        nullable: t.Optional[bool] = None,
        coerce: t.Optional[bool] = None,
        nan: t.Optional[bool] = None,
        inf: t.Optional[bool] = None,
        min: t.Optional[float] = None,
        max: t.Optional[float] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...


class Decimal(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    coerce: t.Optional[bool]
    precision: t.Optional[int]
    nan: t.Optional[bool]
    inf: t.Optional[bool]
    min: t.Optional[float]
    max: t.Optional[float]

    def __init__(
        self,
        *,
        nullable: t.Optional[bool] = None,
        coerce: t.Optional[bool] = None,
        precision: t.Optional[int] = None,
        nan: t.Optional[bool] = None,
        inf: t.Optional[bool] = None,
        min: t.Optional[float] = None,
        max: t.Optional[float] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...
