try:
    import typing as t  # noqa
except ImportError:  # pragma: no cover
    pass

from .. import exc
from . import abstract


class AllOf(abstract.Validator):

    __slots__ = ("steps",)

    def __init__(self, *steps, **kw):
        super(AllOf, self).__init__(steps=list(steps), **kw)

    def __call__(self, value):
        for num, step in enumerate(self.steps):
            try:
                value = step(value)
            except exc.ValidationError as e:
                raise e.add_context(exc.StepNo(num))
        return value


class AnyOf(abstract.Validator):

    __slots__ = ("steps",)

    def __init__(self, *steps, **kw):
        super(AnyOf, self).__init__(steps=list(steps), **kw)

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
