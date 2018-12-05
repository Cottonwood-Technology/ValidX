import sys
import inspect
from copy import deepcopy

from . import classes, instances

if sys.version_info[0] < 3:  # pragma: no cover
    from abc import ABCMeta, abstractmethod

    ABC = ABCMeta("ABC", (object,), {})
else:  # pragma: no cover
    from abc import ABC, abstractmethod


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

    :param \**kw:
        concrete validator attributes.

    """

    __slots__ = ()

    def __init__(self, alias=None, replace=False, **kw):
        for slot in self.__slots__:
            kw.setdefault(slot, None)
        for slot, value in kw.items():
            setattr(self, slot, value)
        if alias is not None:
            if replace:
                instances.put(alias, self)
            else:
                instances.add(alias, self)

    @abstractmethod
    def __call__(self, value):
        """
        Validate value.

        This is an abstract method,
        and it should be implemented by descendant class.

        """

    def __repr__(self):
        params = ", ".join("%s=%r" % (slot, value) for slot, value in self.params())
        return "<%s(%s)>" % (self.__class__.__name__, params)

    def __eq__(self, other):
        return self.__class__ is other.__class__ and tuple(self.params()) == tuple(
            other.params()
        )

    def params(self):
        for slot in self.__slots__:
            if slot.startswith("_"):
                continue
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
            if isinstance(value, dict):
                return {k: _dump(v) for k, v in value.items()}
            if isinstance(value, (list, tuple)):
                type_ = type(value)
                return type_(_dump(i) for i in value)
            if inspect.ismethod(value) or inspect.isfunction(value):
                return value
            return deepcopy(value)

        result = {"__class__": self.__class__.__name__}
        for slot, value in self.params():
            result[slot] = _dump(value)
        return result

    @staticmethod
    def load(params, update=None, unset=None):
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
            ...         "/": {"min": -100},
            ...     },
            ... })
            <Int(min=-100, max=100)>

        """
        assert isinstance(params, dict), "Expected %r, got %r" % (dict, type(params))
        assert "__class__" in params or "__use__" in params or "__clone__" in params, (
            "One of keys ['__class__', '__use__', '__clone__'] must be specified in: %r"
            % params
        )
        return _load_recurcive(params, update, unset)

    def clone(self, update=None, unset=None):
        """
        Clone validator.

        ..  testsetup:: clone

            from validx import Int

        ..  doctest:: clone

            >>> some_enum = Int(options=(1, 2, 3, 4, 5))
            >>> some_enum
            <Int(options=(1, 2, 3, 4, 5))>

            >>> some_enum.clone(
            ...     update={
            ...         "/": {"nullable": True},
            ...         "/options": {0: 10, 2: 30},
            ...     },
            ...     unset={
            ...         "/options": (1, 3),
            ...     }
            ... )
            <Int(nullable=True, options=(10, 30, 5))>


        In fact, the method is a shortcut for:

        ..  code-block:: python

            self.load(self.dump(), update, unset)

        """
        return self.load(self.dump(), update, unset)


def _load_recurcive(params, update, unset, path=()):
    if isinstance(params, dict):
        result = _merge_dict(params, update, unset, path)
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
    if isinstance(params, list):
        return _merge_list(params, update, unset, path)
    if isinstance(params, tuple):
        return tuple(_merge_list(params, update, unset, path))
    return params


def _merge_dict(params, update, unset, path):
    if update is not None or unset is not None:
        params = dict(params)  # make a copy
        path_key = "/%s" % "/".join(str(node) for node in path)

        if update is not None and path_key in update:
            params.update(update[path_key])

        if unset is not None and path_key in unset:
            for key in unset[path_key]:
                params.pop(key, None)

    return {
        key: _load_recurcive(value, update, unset, path + (key,))
        for key, value in params.items()
    }


def _merge_list(params, update, unset, path):
    this_update = None
    this_unset = None

    if update is not None or unset is not None:
        path_key = "/%s" % "/".join(str(node) for node in path)
        if update is not None and path_key in update:
            this_update = update[path_key]
        if unset is not None and path_key in unset:
            this_unset = unset[path_key]

    result = []
    last_num = 0
    for num, value in enumerate(params):
        if this_unset is not None and num in this_unset:
            continue
        if this_update is not None and num in this_update:
            value = this_update[num]
        result.append(_load_recurcive(value, update, unset, path + (num,)))
        last_num = num

    if this_update is not None and "extend" in this_update:
        result.extend(
            # It makes no sense to update or unset from additional elements.
            # So that ``update`` and ``unset`` parameter are not passed.
            _load_recurcive(value, None, None, path + (last_num + num,))
            for num, value in enumerate(this_update["extend"])
        )

    return result
