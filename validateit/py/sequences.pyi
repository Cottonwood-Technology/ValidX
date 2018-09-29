import typing as t
from . import abstract

class List(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    item: abstract.Validator
    nullable: t.Optional[bool]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]
    unique: t.Optional[bool]
    def __init__(
        self,
        item: abstract.Validator,
        *,
        nullable: bool = None,
        minlen: int = None,
        maxlen: int = None,
        unique: bool = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[t.List]: ...

class Tuple(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    items: t.List[abstract.Validator]
    nullable: t.Optional[bool]
    def __init__(
        self,
        *items: abstract.Validator,
        nullable: bool = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[t.Tuple]: ...
