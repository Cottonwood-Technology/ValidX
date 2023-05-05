import typing as t
from abc import ABC

Value = t.TypeVar("Value")


class Validator(ABC):
    __slots__: t.Tuple[str, ...]

    def __init__(
        self, *, alias: t.Optional[str] = None, replace: bool = False, **kw
    ) -> None:
        ...

    def __call__(self, value: Value) -> Value:
        ...

    def __repr__(self) -> str:
        ...

    def __eq__(self, other: t.Any) -> bool:
        ...

    def params(self) -> t.Iterator[t.Tuple[str, t.Any]]:
        ...

    def dump(self) -> t.Dict[str, t.Any]:
        ...

    @staticmethod
    def load(
        params: t.Dict[str, t.Any],
        update: t.Optional[t.Dict[str, t.Any]] = None,
        **kw,
    ) -> Validator:
        ...

    def clone(self, update: t.Optional[t.Dict[str, t.Any]] = None, **kw) -> Validator:
        ...
