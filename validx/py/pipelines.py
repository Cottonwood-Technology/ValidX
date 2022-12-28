from .. import contracts
from .. import exc
from . import abstract


class AllOf(abstract.Validator):
    """
    AND-style Pipeline Validator

    All steps must be succeeded.
    The last step returns result.


    :param Validator \\*steps:
        nested validators.

    :raises ValidationError:
        raised by the first failed step.

    :note:
        it uses :class:`validx.exc.Step` marker to indicate,
        which step is failed.

    """

    __slots__ = ("steps",)

    def __init__(self, *steps_, steps=None, alias=None, replace=False):
        steps = contracts.expect_sequence(
            self, "steps", steps or steps_, item_type=abstract.Validator
        )

        setattr = object.__setattr__
        setattr(self, "steps", steps)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if __context is None:
            __context = {}  # Setup context, if it's top level call

        for num, step in enumerate(self.steps):
            try:
                value = step(value, __context)
            except exc.ValidationError as e:
                raise e.add_context(exc.Step(num))
        return value


class OneOf(abstract.Validator):
    """
    OR-style Pipeline Validator

    The first succeeded step returns result.


    :param Validator \\*steps:
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

    def __init__(self, *steps_, steps=None, alias=None, replace=False):
        steps = contracts.expect_sequence(
            self, "steps", steps or steps_, item_type=abstract.Validator
        )

        setattr = object.__setattr__
        setattr(self, "steps", steps)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if __context is None:
            __context = {}  # Setup context, if it's top level call

        errors = []
        for num, step in enumerate(self.steps):
            try:
                return step(value, __context)
            except exc.ValidationError as e:
                errors.extend(ne.add_context(exc.Step(num)) for ne in e)
        if errors:
            raise exc.SchemaError(errors)
