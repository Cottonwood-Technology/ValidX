import typing as t
from . import abstract

class Bool(abstract.Validator):
    TRUE: t.ClassVar[t.Tuple[str, ...]]
    FALSE: t.ClassVar[t.Tuple[str, ...]]
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    coerce_str: t.Optional[bool]
    coerce_int: t.Optional[bool]
    def __init__(
        self,
        *,
        nullable: bool = None,
        coerce_str: bool = None,
        coerce_int: bool = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...
