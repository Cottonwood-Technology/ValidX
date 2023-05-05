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
        nullable: t.Optional[bool] = None,
        minlen: t.Optional[int] = None,
        maxlen: t.Optional[int] = None,
        unique: t.Optional[bool] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...


class Set(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    item: abstract.Validator
    nullable: t.Optional[bool]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]

    def __init__(
        self,
        item: abstract.Validator,
        *,
        nullable: t.Optional[bool] = None,
        minlen: t.Optional[int] = None,
        maxlen: t.Optional[int] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...


class Tuple(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    items: t.List[abstract.Validator]
    nullable: t.Optional[bool]

    def __init__(
        self,
        *items: abstract.Validator,
        nullable: t.Optional[bool] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...


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
        schema: t.Optional[t.Dict[t.Any, abstract.Validator]] = None,
        *,
        nullable: t.Optional[bool] = None,
        minlen: t.Optional[int] = None,
        maxlen: t.Optional[int] = None,
        extra: t.Optional[t.Tuple[abstract.Validator, abstract.Validator]] = None,
        defaults: t.Optional[t.Dict] = None,
        optional: t.Optional[t.Container] = None,
        dispose: t.Optional[t.Container] = None,
        multikeys: t.Optional[t.Container] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...
