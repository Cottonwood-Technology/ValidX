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
