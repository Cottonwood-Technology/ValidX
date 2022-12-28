import typing as t

from .errors import ValidationError

SimpleTemplate = str
Predicate = t.Callable[[ValidationError], bool]
ConditionalTemplate = t.Tuple[Predicate, SimpleTemplate]
AnyTemplate = t.Union[
    SimpleTemplate, t.List[t.Union[ConditionalTemplate, SimpleTemplate]]
]
Templates = t.Dict[t.Type[ValidationError], AnyTemplate]

class Formatter:
    def __init__(self, templates: Templates) -> None: ...
    def __call__(self, error: ValidationError) -> t.List[t.Tuple[str, str]]: ...

format_error: Formatter
