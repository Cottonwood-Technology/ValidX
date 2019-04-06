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
        nullable: bool = None,
        coerce: bool = None,
        min: int = None,
        max: int = None,
        options: t.Container[int] = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...

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
        nullable: bool = None,
        coerce: bool = None,
        nan: bool = None,
        inf: bool = None,
        min: float = None,
        max: float = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...
