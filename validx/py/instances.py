"""Instance Registry"""


_instances = {}


def add(alias, instance):
    """
    Add validator into the registry


    :param str alias:
        alias of the validator.

    :param Validator instance:
        instance of the validator.


    :raises AssertionError:
        if there is an instance in the registry with the same alias.


    :returns:
        unmodified instance of passed validator.

    """
    assert alias not in _instances, "Alias '%s' of %r conflicts with %r" % (
        alias,
        instance,
        _instances[alias],
    )
    _instances[alias] = instance
    return instance


def put(alias, instance):
    """
    Put validator into the registry

    The function silently replaces any instance with the same alias.


    :param str alias:
        alias of the validator.

    :param Validator instance:
        instance of the validator.


    :returns:
        unmodified instance of passed validator.

    """
    _instances[alias] = instance
    return instance


def get(alias):
    """
    Get validator from the registry


    :param str alias:
        alias of the validator.


    :raises KeyError:
        if there is no registered validator under the specified alias.


    :returns:
        previously registered validator.

    """
    try:
        return _instances[alias]
    except KeyError:
        raise KeyError("Instance '%s' is not registered" % alias)


def clear():
    """Clear the registry"""
    _instances.clear()
