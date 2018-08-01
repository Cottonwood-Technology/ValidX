cdef _instances = {}


cpdef add(str alias, instance):
    assert alias not in _instances, "Alias '%s' of %r conflicts with %r" % (
        alias,
        instance,
        _instances[alias],
    )
    _instances[alias] = instance
    return instance


cpdef put(str alias, instance):
    _instances[alias] = instance
    return instance


cpdef get(str alias):
    try:
        return _instances[alias]
    except KeyError:
        raise KeyError("Instance '%s' is not registered" % alias)


cpdef clear():
    _instances.clear()
