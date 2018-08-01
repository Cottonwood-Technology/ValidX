from .. import exc
from . cimport abstract, instances


cdef class LazyRef(abstract.Validator):

    __slots__ = ("use", "maxdepth", "_depth")

    cdef public str use
    cdef int _maxdepth
    cdef public int _depth

    @property
    def maxdepth(self):
        return None if self._maxdepth == 0 else self._maxdepth

    @maxdepth.setter
    def maxdepth(self, value):
        self._maxdepth = value if value is not None else 0

    def __init__(self, use, **kw):
        super(LazyRef, self).__init__(use=use, _depth=0, **kw)

    def __call__(self, value):
        try:
            self._depth += 1
            if self._maxdepth > 0 and self._depth > self._maxdepth:
                raise exc.RecursionMaxDepthError(
                    expected=self._maxdepth, actual=self._depth
                )
            return instances.get(self.use)(value)
        finally:
            self._depth -= 1
