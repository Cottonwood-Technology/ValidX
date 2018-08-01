import typing as t
from . import abstract

class AllOf(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    steps: t.List[abstract.Validator]
    def __init__(
        self, *steps: abstract.Validator, alias: str = None, replace: bool = False
    ) -> None: ...

class AnyOf(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    steps: t.List[abstract.Validator]
    def __init__(
        self, *steps: abstract.Validator, alias: str = None, replace: bool = False
    ) -> None: ...
