_instances = {}


def add(alias, instance):
    assert alias not in _instances, "Alias '%s' of %r conflicts with %r" % (
        alias,
        instance,
        _instances[alias],
    )
    _instances[alias] = instance
    return instance


def put(alias, instance):
    _instances[alias] = instance
    return instance


def get(alias):
    try:
        return _instances[alias]
    except KeyError:
        raise KeyError("Instance '%s' is not registered" % alias)


def clear():
    _instances.clear()
