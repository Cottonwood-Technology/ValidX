import typing as t
from abc import ABC
from datetime import date, time, datetime, timedelta

class Validator(ABC):
    __slots__: t.Tuple[str, ...]
    def __init__(self, *, alias: str = None, **kw) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[t.Any]: ...
    def __repr__(self) -> str: ...
    def params(self) -> t.Iterator[t.Tuple[str, t.Any]]: ...
    def dump(self) -> t.Dict[str, t.Any]: ...
    def clone(
        self, update: t.Dict[str, t.Dict] = None, unset: t.Dict[str, t.Container] = None
    ) -> Validator: ...

class Any(Validator):
    __slots__: t.Tuple[str, ...]
    def __init__(self, *, nullable: bool = None, alias: str = None) -> None: ...

class Int(Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    coerce: t.Optional[bool]
    min: t.Optional[int]
    max: t.Optional[int]
    options: t.Optional[t.Container[int]]
    def __init__(
        self,
        *,
        nullable: bool = None,
        coerce: bool = None,
        min: int = None,
        max: int = None,
        options: t.Container[int] = None,
        alias: str = None,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[int]: ...

class Float(Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    coerce: t.Optional[bool]
    nan: t.Optional[bool]
    inf: t.Optional[bool]
    min: t.Optional[float]
    max: t.Optional[float]
    def __init__(
        self,
        *,
        nullable: bool = None,
        coerce: bool = None,
        nan: bool = None,
        inf: bool = None,
        min: float = None,
        max: float = None,
        alias: str = None,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[float]: ...

class Str(Validator):
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
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[str]: ...

class Bytes(Validator):
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
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[bytes]: ...

class Date(Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    unixts: t.Optional[bool]
    format: t.Optional[str]
    min: t.Optional[date]
    max: t.Optional[date]
    relmin: t.Optional[timedelta]
    relmax: t.Optional[timedelta]
    def __init__(
        self,
        *,
        nullable: bool = None,
        unixts: bool = None,
        format: str = None,
        min: date = None,
        max: date = None,
        relmin: timedelta = None,
        relmax: timedelta = None,
        alias: str = None,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[date]: ...

class Time(Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    format: t.Optional[str]
    min: t.Optional[time]
    max: t.Optional[time]
    def __init__(
        self,
        *,
        nullable: bool = None,
        format: str = None,
        min: time = None,
        max: time = None,
        alias: str = None,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[time]: ...

class Datetime(Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    unixts: t.Optional[bool]
    format: t.Optional[str]
    min: t.Optional[datetime]
    max: t.Optional[datetime]
    relmin: t.Optional[timedelta]
    relmax: t.Optional[timedelta]
    def __init__(
        self,
        *,
        nullable: bool = None,
        unixts: bool = None,
        format: str = None,
        min: datetime = None,
        max: datetime = None,
        relmin: timedelta = None,
        relmax: timedelta = None,
        alias: str = None,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[datetime]: ...

class Bool(Validator):
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
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[bool]: ...

class List(Validator):

    __slots__: t.Tuple[str, ...]

    item: Validator
    nullable: t.Optional[bool]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]
    unique: t.Optional[bool]
    def __init__(
        self,
        item: Validator,
        *,
        nullable: bool = None,
        minlen: int = None,
        maxlen: int = None,
        unique: bool = None,
        alias: str = None,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[t.List]: ...

class Sequence(Validator):
    __slots__: t.Tuple[str, ...]
    item: Validator
    nullable: t.Optional[bool]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]
    unique: t.Optional[bool]
    def __init__(
        self,
        item: Validator,
        *,
        nullable: bool = None,
        minlen: int = None,
        maxlen: int = None,
        unique: bool = None,
        alias: str = None,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[t.List]: ...

class Tuple(Validator):
    __slots__: t.Tuple[str, ...]
    items: t.List[Validator]
    nullable: t.Optional[bool]
    def __init__(
        self, *items: Validator, nullable: bool = None, alias: str = None
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[t.Tuple]: ...

class Dict(Validator):
    __slots__: t.Tuple[str, ...]
    schema: t.Dict[t.Any, Validator]
    nullable: t.Optional[bool]
    extra: t.Optional[t.Tuple[Validator, Validator]]
    defaults: t.Optional[t.Dict]
    optional: t.Optional[t.Container]
    dispose: t.Optional[t.Container]
    def __init__(
        self,
        schema: t.Dict[t.Any, Validator],
        *,
        nullable: bool = None,
        extra: Tuple = None,
        defaults: t.Dict = None,
        optional: t.Container = None,
        dispose: t.Container = None,
        alias: str = None,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[t.Dict]: ...

class Mapping(Validator):
    __slots__: t.Tuple[str, ...]
    schema: t.Dict[t.Any, Validator]
    nullable: t.Optional[bool]
    extra: t.Optional[t.Tuple[Validator, Validator]]
    defaults: t.Optional[t.Dict]
    optional: t.Optional[t.Container]
    dispose: t.Optional[t.Container]
    multikeys: t.Optional[t.Container]
    def __init__(
        self,
        schema: t.Dict[t.Any, Validator],
        *,
        nullable: bool = None,
        extra: Tuple = None,
        defaults: t.Dict = None,
        optional: t.Container = None,
        dispose: t.Container = None,
        multikeys: t.Container = None,
        alias: str = None,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[t.Dict]: ...

class AllOf(Validator):
    __slots__: t.Tuple[str, ...]
    steps: t.List[Validator]
    def __init__(self, *steps: Validator, alias: str = None) -> None: ...

class AnyOf(Validator):
    __slots__: t.Tuple[str, ...]
    steps: t.List[Validator]
    def __init__(self, *steps: Validator, alias: str = None) -> None: ...
