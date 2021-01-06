import typing as t

class Extra(object):
    __slots__: t.Tuple[str, ...]
    name: str
    def __init__(self, name: str) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: t.Any) -> bool: ...

class Step(object):
    __slots__: t.Tuple[str, ...]
    num: int
    def __init__(self, num: int) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: t.Any) -> bool: ...

EXTRA_KEY: Extra
EXTRA_VALUE: Extra