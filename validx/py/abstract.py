from warnings import warn
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence, Container

from . import classes, instances
from ..types import chars


class Validator(ABC):
    """
    Abstract Base Validator

    :param str alias:
        if it specified,
        the instance will be added into registry,
        see :func:`validx.py.instances.add`.

    :param bool replace:
        if it is ``True`` and ``alias`` specified,
        the instance will be added into registry,
        replacing any existent validator with the same alias,
        see :func:`validx.py.instances.put`.

    :param \\**kw:
        concrete validator attributes.

    """

    __slots__ = ()

    def __init__(self, alias=None, replace=False):
        self._register(alias, replace)

    def _register(self, alias=None, replace=False):
        if alias is not None:
            if replace:
                instances.put(alias, self)
            else:
                instances.add(alias, self)

    @abstractmethod
    def __call__(self, value, __context=None):
        """
        Validate value.

        This is an abstract method,
        and it should be implemented by descendant class.

        """

    def __setattr__(self, name, value):  # pragma: no cover
        raise NotImplementedError("%s object is immutable", self.__class__)

    def __repr__(self):
        params = ", ".join("%s=%r" % (slot, value) for slot, value in self.params())
        return "<%s(%s)>" % (self.__class__.__name__, params)

    def __eq__(self, other):
        return self.__class__ is other.__class__ and tuple(self.params()) == tuple(
            other.params()
        )

    def __reduce__(self):
        return (_load_recurcive, (self.dump(),))

    def params(self):
        for slot in self.__slots__:
            value = getattr(self, slot)
            if value is not None and value is not False:
                yield slot, value

    def dump(self):
        """
        Dump validator.

        ..  testsetup:: dump

            from validx import Int

        ..  doctest:: dump

            >>> Int(min=0, max=100).dump() == {
            ...     "__class__": "Int",
            ...     "min": 0,
            ...     "max": 100,
            ... }
            True

        """

        def _dump(value):
            if isinstance(value, Validator):
                return value.dump()
            if isinstance(value, Mapping):
                return {k: _dump(v) for k, v in value.items()}
            if isinstance(value, Sequence) and not isinstance(value, chars):
                return [_dump(i) for i in value]
            if isinstance(value, Container) and not isinstance(value, chars):
                return set(value)
            return value

        result = {"__class__": self.__class__.__name__}
        for slot, value in self.params():
            result[slot] = _dump(value)
        return result

    @staticmethod
    def load(params, update=None, unset=None, **kw):
        """
        Load validator.

        ..  testsetup:: load

            from validx import Validator, Int, instances

        ..  testcleanup:: load

            instances.clear()

        ..  doctest:: load

            >>> Validator.load({
            ...     "__class__": "Int",
            ...     "min": 0,
            ...     "max": 100,
            ... })
            <Int(min=0, max=100)>

            >>> # Add into registry
            >>> some_int = Validator.load({
            ...     "__class__": "Int",
            ...     "min": 0,
            ...     "max": 100,
            ...     "alias": "some_int",
            ... })
            >>> some_int
            <Int(min=0, max=100)>

            >>> # Load from registry by alias
            >>> Validator.load({"__use__": "some_int"}) is some_int
            True

            >>> # Clone from registry by alias
            >>> Validator.load({
            ...     "__clone__": "some_int",
            ...     "update": {
            ...         "min": -100,
            ...     },
            ... })
            <Int(min=-100, max=100)>

        """
        assert isinstance(params, dict), "Expected %r, got %r" % (dict, type(params))
        assert "__class__" in params or "__use__" in params or "__clone__" in params, (
            "One of keys ['__class__', '__use__', '__clone__'] must be specified in: %r"
            % params
        )

        _update = {}
        _unset = {}

        if update is not None:
            for key, value in update.items():
                if key.startswith("/"):
                    key = key.replace("/", ".").lstrip(".")
                    _update[key] = value
                    warn(
                        "This syntax is deprecated. "
                        "Consider to use '%s+' instead." % key,
                        DeprecationWarning,
                    )
                elif key.endswith("+"):
                    key = key.rstrip("+")
                    _update[key] = value
                elif key.endswith("-"):
                    key = key.rstrip("-")
                    _unset[key] = value
                else:
                    context_key, value_key = (
                        key.rsplit(".", 1) if "." in key else ("", key)
                    )
                    _update.setdefault(context_key, {})[value_key] = value
        if kw:
            _update.setdefault("", {}).update(kw)

        if unset is not None:
            for key, value in unset.items():
                key = key.replace("/", ".").lstrip(".")
                _unset[key] = value
                warn(
                    "This syntax is deprecated. "
                    "Consider to use '%s-' instead "
                    "and place it into update param." % key,
                    DeprecationWarning,
                )

        return _load_recurcive(params, _update, _unset)

    def clone(self, update=None, unset=None, **kw):
        """
        Clone validator.

        ..  testsetup:: clone

            from validx import Int

        ..  doctest:: clone

            >>> some_enum = Int(options=[1, 2, 3])
            >>> some_enum.clone(
            ...     {
            ...         "nullable": True,
            ...         "options+": [4, 5],
            ...         "options-": [1, 2],
            ...     }
            ... ) == Int(nullable=True, options=[3, 4, 5])
            True


        In fact, the method is a shortcut for:

        ..  code-block:: python

            self.load(self.dump(), update, **kw)

        """
        return self.load(self.dump(), update, unset, **kw)


def _load_recurcive(params, update=None, unset=None, path=()):
    path_key = ".".join(path)
    update_this = update.get(path_key) if update is not None else None
    unset_this = unset.get(path_key) if unset is not None else None

    if isinstance(params, dict):
        result = {
            key: _load_recurcive(value, update, unset, path + (str(key),))
            for key, value in params.items()
        }
        if update_this is not None:
            result.update(
                {key: _load_recurcive(value) for key, value in update_this.items()}
            )
        if unset_this is not None:
            for key in unset_this:
                try:
                    del result[key]
                except KeyError:
                    raise KeyError("%r is not in dict at '%s'" % (key, path_key))
        if "__class__" in result:
            classname = result.pop("__class__")
            class_ = classes.get(classname)
            return class_(**result)
        if "__clone__" in result:
            alias = result.pop("__clone__")
            instance = instances.get(alias)
            return instance.clone(**result)
        if "__use__" in result:
            return instances.get(result["__use__"])
        return result

    if isinstance(params, set):
        result = set(params)
        if update_this is not None:
            result.update(update_this)
        if unset_this is not None:
            for value in unset_this:
                try:
                    result.remove(value)
                except KeyError:
                    raise KeyError("%r is not in set at '%s'" % (value, path_key))
        return result

    if isinstance(params, list):
        result = [
            _load_recurcive(value, update, unset, path + (str(num),))
            for num, value in enumerate(params)
        ]
        if update_this is not None:
            result.extend(_load_recurcive(value) for value in update_this)
        if unset_this is not None:
            for value in unset_this:
                value = _load_recurcive(value)
                try:
                    result.remove(value)
                except ValueError:
                    raise ValueError("%r is not in list at '%s'" % (value, path_key))
        return result

    return params
