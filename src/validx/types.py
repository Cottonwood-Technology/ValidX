from collections.abc import Mapping


__all__ = ["numbers", "chars", "frozendict"]


numbers = (int, float)
chars = (str, bytes)


class frozendict(Mapping):
    def __init__(self, *args, **kw):
        self.__data = dict(*args, **kw)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__data)

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
