import typing as t
from abc import abstractmethod, ABC


class Validator(ABC):

    __slots__: t.Tuple[str, ...]

    def __init__(self, **kw) -> None:
        ...

    @abstractmethod
    def __call__(self, value: t.Any) -> t.Optional[t.Any]:
        ...

    def dump(self) -> t.Dict[str, t.Any]:
        ...


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
    ) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[int]:
        ...


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
    ) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[float]:
        ...


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
    ) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[str]:
        ...


class Bytes(Validator):

    __slots__: t.Tuple[str, ...]

    nullable: t.Optional[bool]
    minlen: t.Optional[int]
    maxlen: t.Optional[int]

    def __init__(
        self, *, nullable: bool = None, minlen: int = None, maxlen: int = None
    ) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[bytes]:
        ...


class Bool(Validator):

    TRUE: t.ClassVar[t.Tuple[str, ...]]
    FALSE: t.ClassVar[t.Tuple[str, ...]]

    __slots__: t.Tuple[str, ...]

    nullable: t.Optional[bool]
    coerce_str: t.Optional[bool]
    coerce_int: t.Optional[bool]

    def __init__(
        self, *, nullable: bool = None, coerce_str: bool = None, coerce_int: bool = None
    ) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[bool]:
        ...


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
    ) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[t.List]:
        ...


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
    ) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[t.List]:
        ...


class Tuple(Validator):

    __slots__: t.Tuple[str, ...]

    items: t.List[Validator]
    nullable: t.Optional[bool]

    def __init__(self, *items: Validator, nullable: bool = None) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[t.Tuple]:
        ...


class Dict(Validator):

    __slots__: t.Tuple[str, ...]

    schema: t.Dict[t.Any, Validator]
    nullable: t.Optional[bool]
    extra: t.Optional[Tuple]
    defaults: t.Optional[t.Dict]
    optional: t.Optional[t.Container]

    def __init__(
        self,
        schema: t.Dict[t.Any, Validator],
        nullable: bool = None,
        extra: Tuple = None,
        defaults: t.Dict = None,
        optional: t.Container = None,
    ) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[t.Dict]:
        ...


class Mapping(Validator):

    __slots__: t.Tuple[str, ...]

    schema: t.Dict[t.Any, Validator]
    nullable: t.Optional[bool]
    extra: t.Optional[Tuple]
    defaults: t.Optional[t.Dict]
    optional: t.Optional[t.Container]

    def __init__(
        self,
        schema: t.Dict[t.Any, Validator],
        nullable: bool = None,
        extra: Tuple = None,
        defaults: t.Dict = None,
        optional: t.Container = None,
    ) -> None:
        ...

    def __call__(self, value: t.Any) -> t.Optional[t.Dict]:
        ...
