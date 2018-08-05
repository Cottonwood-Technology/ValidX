"""Class Registry"""


_classes = {}


def add(class_):
    """
    Add validator class into the registry


    :param Validator class_:
        class to register.


    :raises AssertionError:
        if there is a class in the registry with the same name,
        i.e. ``class_.__name__``.


    :returns:
        unmodified passed class,
        so the function can be used as a decorator.

    """
    assert class_.__name__ not in _classes, "Name of %r conflicts with %r" % (
        class_,
        _classes[class_.__name__],
    )
    _classes[class_.__name__] = class_
    return class_


def get(classname):
    """
    Get validator class from the registry

    :param str classname:
        name of class to get.

    :raises KeyError:
        if there is no class in the registry with the specified name.

    :returns:
        previously registered class.

    """
    try:
        return _classes[classname]
    except KeyError:
        raise KeyError("Class '%s' is not registered" % classname)
