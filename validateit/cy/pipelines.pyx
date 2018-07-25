from .. import exc
from . cimport abstract


cdef class AllOf(abstract.Validator):

    __slots__ = ("steps",)

    cdef public steps

    def __init__(self, *steps, **kw):
        super(AllOf, self).__init__(steps=list(steps), **kw)

    def __call__(self, value):
        for num, step in enumerate(self.steps):
            try:
                value = step(value)
            except exc.ValidationError as e:
                raise e.add_context(exc.StepNo(num))
        return value


cdef class AnyOf(abstract.Validator):

    __slots__ = ("steps",)

    cdef public steps

    def __init__(self, *steps, **kw):
        super(AnyOf, self).__init__(steps=list(steps), **kw)

    def __call__(self, value):
        errors = []
        for num, step in enumerate(self.steps):
            try:
                return step(value)
            except exc.ValidationError as e:
                errors.extend(ne.add_context(exc.StepNo(num)) for ne in e)
        if errors:
            raise exc.SchemaError(errors)
        # If there are no steps, return value as it is.
        return value
