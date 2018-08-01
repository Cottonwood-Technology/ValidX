cdef _classes = {}


cpdef add(class_):
    assert class_.__name__ not in _classes, "Name of %r conflicts with %r" % (
        class_,
        _classes[class_.__name__],
    )
    _classes[class_.__name__] = class_
    return class_


cpdef get(str classname):
    try:
        return _classes[classname]
    except KeyError:
        raise KeyError("Class '%s' is not registered" % classname)
