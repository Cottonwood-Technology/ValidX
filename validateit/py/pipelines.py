try:
    import typing as t  # noqa
except ImportError:  # pragma: no cover
    pass

from .. import exc
from . import abstract


class AllOf(abstract.Validator):
    """
    AND-style Pipeline Validator

    All steps must be succeeded.
    The last step returns result.


    :param Validator \*steps:
        nested validators.


    :raises ValidationError:
        raised by the first failed step.


    :warning:
        If there are no steps,
        value **will not be validated** and **no error will be raised**.

    """

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
    """
    OR-style Pipeline Validator

    The first succeeded step returns result.


    :param Validator \*steps:
        nested validators.

    :raises SchemaError:
        if all steps are failed,
        so it contains all errors,
        raised by each step.


    :warning:
        If there are no steps,
        value **will not be validated** and **no error will be raised**.

    """

    __slots__ = ("steps",)

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
        return value  # pragma: no cover
