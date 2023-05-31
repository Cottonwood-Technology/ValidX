import typing as t
from . import abstract


class Str(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    coerce: t.Optional[bool]
    dontstrip: t.Optional[bool]
    normspace: t.Optional[bool]
    encoding: t.Optional[str]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]
    pattern: t.Optional[str]
    options: t.Optional[t.Container[str]]

    def __init__(
        self,
        *,
        nullable: t.Optional[bool] = None,
        coerce: t.Optional[bool] = None,
        dontstrip: t.Optional[bool] = None,
        normspace: t.Optional[bool] = None,
        encoding: t.Optional[str] = None,
        minlen: t.Optional[int] = None,
        maxlen: t.Optional[int] = None,
        pattern: t.Optional[str] = None,
        options: t.Optional[t.Container[str]] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...


class Bytes(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]

    def __init__(
        self,
        *,
        nullable: t.Optional[bool] = None,
        minlen: t.Optional[int] = None,
        maxlen: t.Optional[int] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...
