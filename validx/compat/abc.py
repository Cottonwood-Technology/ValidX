from __future__ import absolute_import


__all__ = ["ABC", "abstractmethod"]


try:
    from abc import ABC, abstractmethod
except ImportError:  # pragma: no cover
    from abc import ABCMeta, abstractmethod

    ABC = ABCMeta("ABC", (object,), {})  # type: ignore
