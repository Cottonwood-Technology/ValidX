import typing as t
from . import abstract

class Str(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    encoding: t.Optional[str]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]
    pattern: t.Optional[str]
    options: t.Optional[t.Container[str]]
    def __init__(
        self,
        *,
        nullable: bool = None,
        encoding: str = None,
        minlen: int = None,
        maxlen: int = None,
        pattern: str = None,
        options: t.Container[str] = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...

class Bytes(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]
    def __init__(
        self,
        *,
        nullable: bool = None,
        minlen: int = None,
        maxlen: int = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...
