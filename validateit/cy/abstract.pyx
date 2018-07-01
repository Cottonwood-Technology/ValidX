cdef class Validator:

    __slots__ = ()

    def __init__(self, **kw):
        for slot in self.__slots__:
            kw.setdefault(slot, None)
        for slot, value in kw.items():
            setattr(self, slot, value)

    def dump(self):
        result = {}
        for slot in self.__slots__:
            value = getattr(self, slot)
            if value is not None and value is not False:
                result[slot] = value
        return result
