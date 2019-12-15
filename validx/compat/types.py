import sys


__all__ = ["numbers", "chars", "string", "basestr"]


numbers = (int, float)


if sys.version_info[0] > 2:
    chars = (str, bytes)
    string = str
    basestr = str
else:  # pragma: no cover
    chars = (unicode, bytes)  # noqa
    string = unicode  # noqa
    basestr = basestring  # noqa
