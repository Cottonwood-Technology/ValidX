import sys

if sys.version_info[0] < 3:  # pragma: no cover
    from abc import ABCMeta, abstractmethod

    ABC = ABCMeta("ABC", (object,), {})
else:  # pragma: no cover
    from abc import ABC, abstractmethod


class Validator(ABC):

    __slots__ = ()

    def __init__(self, **kw):
        for slot in self.__slots__:
            kw.setdefault(slot, None)
        for slot, value in kw.items():
            setattr(self, slot, value)

    @abstractmethod
    def __call__(self, value):
        pass

    def dump(self):
        result = {}
        for slot in self.__slots__:
            value = getattr(self, slot)
            if value is not None and value is not False:
                result[slot] = value
        return result
