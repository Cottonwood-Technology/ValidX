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

class Dict(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    schema: t.Optional[t.Dict[t.Any, abstract.Validator]]
    nullable: t.Optional[bool]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]
    extra: t.Optional[t.Tuple[abstract.Validator, abstract.Validator]]
    defaults: t.Optional[t.Dict]
    optional: t.Optional[t.Container]
    dispose: t.Optional[t.Container]
    multikeys: t.Optional[t.Container]
    def __init__(
        self,
        schema: t.Dict[t.Any, abstract.Validator] = None,
        *,
        nullable: bool = None,
        minlen: int = None,
        maxlen: int = None,
        extra: t.Tuple[abstract.Validator, abstract.Validator] = None,
        defaults: t.Dict = None,
        optional: t.Container = None,
        dispose: t.Container = None,
        multikeys: t.Container = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...
