from .. import exc
from . cimport abstract


cdef class All(abstract.Validator):

    __slots__ = ("steps",)

    cdef public steps

    def __init__(self, *steps, **kw):
        super(All, self).__init__(steps=list(steps), **kw)

    def __call__(self, value):
        for num, step in enumerate(self.steps):
            try:
                value = step(value)
            except exc.ValidationError as e:
                raise e.add_context(exc.StepNo(num))
        return value


cdef class Any(abstract.Validator):

    __slots__ = ("steps",)

    cdef public steps

    def __init__(self, *steps, **kw):
        super(Any, self).__init__(steps=list(steps), **kw)

    def __call__(self, value):
        errors = []  # type: t.List[exc.ValidationError]
        for num, step in enumerate(self.steps):
            try:
                return step(value)
            except exc.ValidationError as e:
                errors.extend(ne.add_context(exc.StepNo(num)) for ne in e)
        if errors:
            raise exc.SchemaError(errors)
        # If there are no steps, return value as it is.
        return value  # pragma: no cover
