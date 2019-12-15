from __future__ import absolute_import


__all__ = ["Map"]


try:
    from immutables import Map
except ImportError:  # pragma: no cover
    from .colabc import Mapping

    class Map(Mapping):  # type: ignore
        def __init__(self, *args, **kw):
            self.__data = dict(*args, **kw)

        def __getitem__(self, key):
            return self.__data[key]

        def __iter__(self):
            return iter(self.__data)

        def __len__(self):
            return len(self.__data)

        def __contains__(self, key):
            return key in self.__data

        def keys(self):
            return self.__data.keys()

        def items(self):
            return self.__data.items()

        def values(self):
            return self.__data.values()
