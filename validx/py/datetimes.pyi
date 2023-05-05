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
        nullable: t.Optional[bool] = None,
        unixts: t.Optional[bool] = None,
        format: t.Optional[str] = None,
        parser: t.Optional[t.Callable[[str], datetime]] = None,
        min: t.Optional[date] = None,
        max: t.Optional[date] = None,
        relmin: t.Optional[timedelta] = None,
        relmax: t.Optional[timedelta] = None,
        tz: t.Optional[tzinfo] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...


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
        nullable: t.Optional[bool] = None,
        format: t.Optional[str] = None,
        parser: t.Optional[t.Callable[[str], datetime]] = None,
        min: t.Optional[time] = None,
        max: t.Optional[time] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...


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
        nullable: t.Optional[bool] = None,
        unixts: t.Optional[bool] = None,
        format: t.Optional[str] = None,
        parser: t.Optional[t.Callable[[str], datetime]] = None,
        min: t.Optional[datetime] = None,
        max: t.Optional[datetime] = None,
        relmin: t.Optional[timedelta] = None,
        relmax: t.Optional[timedelta] = None,
        tz: t.Optional[tzinfo] = None,
        alias: t.Optional[str] = None,
        replace: bool = False,
    ) -> None:
        ...
