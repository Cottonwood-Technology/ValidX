import typing as t
from datetime import date, time, datetime, timedelta
from . import abstract

class Date(abstract.Validator):
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
        replace: bool = False,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[date]: ...

class Time(abstract.Validator):
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
        replace: bool = False,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[time]: ...

class Datetime(abstract.Validator):
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
        replace: bool = False,
    ) -> None: ...
    def __call__(self, value: t.Any) -> t.Optional[datetime]: ...
