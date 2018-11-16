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

    :note:
        it uses :class:`validx.exc.Step` marker to indicate,
        which step is failed.

    """

    __slots__ = ("steps",)

    def __init__(self, *steps, **kw):
        kw.setdefault("steps", steps)
        assert kw["steps"], "At least one validation step has to be provided"
        super(AllOf, self).__init__(**kw)

    def __call__(self, value):
        validated = False
        for num, step in enumerate(self.steps):
            validated = True
            try:
                value = step(value)
            except exc.ValidationError as e:
                raise e.add_context(exc.Step(num))
        assert validated, "At least one validation step has to be passed"
        return value


class OneOf(abstract.Validator):
    """
    OR-style Pipeline Validator

    The first succeeded step returns result.


    :param Validator \*steps:
        nested validators.

    :raises SchemaError:
        if all steps are failed,
        so it contains all errors,
        raised by each step.

    :note:
        it uses :class:`validx.exc.Step` marker to indicate,
        which step is failed.

    """

    __slots__ = ("steps",)

    def __init__(self, *steps, **kw):
        kw.setdefault("steps", steps)
        assert kw["steps"], "At least one validation step has to be provided"
        super(OneOf, self).__init__(**kw)

    def __call__(self, value):
        errors = []
        for num, step in enumerate(self.steps):
            try:
                return step(value)
            except exc.ValidationError as e:
                errors.extend(ne.add_context(exc.Step(num)) for ne in e)
        if errors:
            raise exc.SchemaError(errors)
        assert False, "At least one validation step has to be passed"
