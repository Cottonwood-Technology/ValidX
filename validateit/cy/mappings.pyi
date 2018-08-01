import typing as t
from . import abstract

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
        alias: str = None,
        replace: bool = False,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[t.Dict]: ...

class Mapping(abstract.Validator):
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
    def __call__(self, value: t.Any) -> t.Optional[t.Dict]: ...
