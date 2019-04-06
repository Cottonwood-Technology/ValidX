import typing as t
from . import abstract

class LazyRef(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    use: str
    maxdepth: t.Optional[int]
    def __init__(
        self,
        use: str,
        *,
        maxdepth: int = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...

class Type(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    tp: t.Type[t.Any]
    nullable: t.Optional[bool]
    coerce: t.Optional[bool]
    min: t.Optional[t.Any]
    max: t.Optional[t.Any]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]
    options: t.Optional[t.Container[t.Any]]
    def __init__(
        self,
        tp: t.Type[t.Any],
        *,
        nullable: bool = None,
        coerce: bool = None,
        min: t.Any = None,
        max: t.Any = None,
        minlen: int = None,
        maxlen: int = None,
        options: t.Container[t.Any] = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...

class Const(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    value: t.Any
    def __init__(
        self, value: t.Any, *, alias: str = None, replace: bool = False
    ) -> None: ...

class Any(abstract.Validator):
    pass
