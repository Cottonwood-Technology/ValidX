from .. import exc
from . import abstract, instances


class LazyRef(abstract.Validator):

    __slots__ = ("use", "maxdepth", "_depth")

    def __init__(self, use, **kw):
        super(LazyRef, self).__init__(use=use, _depth=0, **kw)

    def __call__(self, value):
        try:
            self._depth += 1
            if self.maxdepth is not None and self._depth > self.maxdepth:
                raise exc.RecursionMaxDepthError(
                    expected=self.maxdepth, actual=self._depth
                )
            return instances.get(self.use)(value)
        finally:
            self._depth -= 1
