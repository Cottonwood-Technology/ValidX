import typing as t
from . import abstract

class LazyRef(abstract.Validator):
    __slots__ = t.Tuple[str, ...]
    use: str
    maxdepth: t.Optional[int]
    def __init__(
        self,
        use: str,
        *,
        maxdepth: int = None,
        alias: str = None,
        replace: bool = False
    ) -> None: ...

class Const(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    value: t.Any
    def __init__(
        self, value: t.Any, *, alias: str = None, replace: bool = False
    ) -> None: ...

class Any(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    def __init__(
        self, *, nullable: bool = None, alias: str = None, replace: bool = False
    ) -> None: ...
