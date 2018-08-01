import typing as t
from . import abstract

class Any(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    def __init__(
        self, *, nullable: bool = None, alias: str = None, replace: bool = False
    ) -> None: ...
