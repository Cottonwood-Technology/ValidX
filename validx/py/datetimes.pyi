import typing as t
from datetime import date, time, datetime, timedelta, tzinfo
from . import abstract

class Date(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    unixts: t.Optional[bool]
    format: t.Optional[str]
    parser: t.Optional[t.Callable[[str], datetime]]
    min: t.Optional[date]
    max: t.Optional[date]
    relmin: t.Optional[timedelta]
    relmax: t.Optional[timedelta]
    tz: t.Optional[tzinfo]
    def __init__(
        self,
        *,
        nullable: bool = None,
        unixts: bool = None,
        format: str = None,
        parser: t.Callable[[str], datetime] = None,
        min: date = None,
        max: date = None,
        relmin: timedelta = None,
        relmax: timedelta = None,
        tz: tzinfo = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...

class Time(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    format: t.Optional[str]
    parser: t.Optional[t.Callable[[str], datetime]]
    min: t.Optional[time]
    max: t.Optional[time]
    def __init__(
        self,
        *,
        nullable: bool = None,
        format: str = None,
        parser: t.Callable[[str], datetime] = None,
        min: time = None,
        max: time = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...

class Datetime(abstract.Validator):
    __slots__: t.Tuple[str, ...]
    nullable: t.Optional[bool]
    unixts: t.Optional[bool]
    format: t.Optional[str]
    parser: t.Optional[t.Callable[[str], datetime]]
    min: t.Optional[datetime]
    max: t.Optional[datetime]
    relmin: t.Optional[timedelta]
    relmax: t.Optional[timedelta]
    tz: t.Optional[tzinfo]
    def __init__(
        self,
        *,
        nullable: bool = None,
        unixts: bool = None,
        format: str = None,
        parser: t.Callable[[str], datetime] = None,
        min: datetime = None,
        max: datetime = None,
        relmin: timedelta = None,
        relmax: timedelta = None,
        tz: tzinfo = None,
        alias: str = None,
        replace: bool = False,
    ) -> None: ...
