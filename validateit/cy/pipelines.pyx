from .. import exc
from . cimport abstract


cdef class AllOf(abstract.Validator):

    __slots__ = ("steps",)

    cdef public steps

    def __init__(self, *steps, **kw):
        assert steps, "At least one validation step has to be provided"
        super(AllOf, self).__init__(steps=list(steps), **kw)

    def __call__(self, value):
        cdef bint validated = False
        for num, step in enumerate(self.steps):
            validated = True
            try:
                value = step(value)
            except exc.ValidationError as e:
                raise e.add_context(exc.StepNo(num))
        assert validated, "At least one validation step has to be passed"
        return value


cdef class AnyOf(abstract.Validator):

    __slots__ = ("steps",)

    cdef public steps

    def __init__(self, *steps, **kw):
        assert steps, "At least one validation step has to be provided"
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
        assert False, "At least one validation step has to be passed"
