from . import errors


class Formatter(object):
    """
    Error Formatter

    :param dict templates:
        templates that will be used to format errors.

    Each key of ``templates`` should be a subclass of
    :class:`validx.exc.ValidationError`.

    Each value of ``templates`` should be a string,
    i.e. simple template,
    or list of conditional templates.

    Conditional template is a tuple ``(predicate, string)``.
    Where ``predicate`` is a callable,
    that accepts :class:`validx.exc.ValidationError`
    and returns boolean value.
    When the predicate evaluates to ``True``,
    its corresponding string will be used as a template.

    Last value of list of conditional templates can be a string,
    i.e. default simple template.

    See ``format_error`` object,
    defined within the module,
    as an example.

    """

    def __init__(self, templates):
        assert isinstance(templates, dict), templates
        for exc_class, template in templates.items():
            assert isinstance(exc_class, type), exc_class
            assert issubclass(exc_class, errors.ValidationError), exc_class
            assert isinstance(template, (str, list, tuple)), template
            if isinstance(template, (list, tuple)):
                for f in template:
                    assert isinstance(f, (str, tuple))
                    if isinstance(f, tuple):
                        assert len(f) == 2, f
                        assert callable(f[0]), f[0]
                        assert isinstance(f[1], str), f[1]
        self._templates = templates

    def __call__(self, error):
        """
        Format Error

        :param ValidationError error:
            error to format.

        :returns:
            list of context/message pairs: ``[(str, str), ...]``.

        """
        result = []
        error.sort()
        for e in error:
            context = e.format_context()
            template = self._templates.get(type(e))
            if template is None:
                result.append((context, e.format_error()))
            elif isinstance(template, str):
                result.append((context, template.format(e)))
            elif isinstance(template, (list, tuple)):
                for f in template:
                    if isinstance(f, tuple) and f[0](e):
                        result.append((context, f[1].format(e)))
                        break
                    elif isinstance(f, str):
                        result.append((context, f.format(e)))
                        break
                else:
                    result.append((context, e.format_error()))
        return result


format_error = Formatter(
    {
        errors.InvalidTypeError: [
            (lambda error: error.actual is type(None), "Value should not be null."),
            "Expected type “{0.expected.__name__}”, got “{0.actual.__name__}”.",
        ],
        errors.OptionsError: [
            (
                lambda error: len(error.expected) == 1,
                "Expected {0.expected[0]}, got {0.actual}.",
            ),
            "Expected one of {0.expected}, got {0.actual}.",
        ],
        errors.MinValueError: "Expected value ≥ {0.expected}, got {0.actual}.",
        errors.MaxValueError: "Expected value ≤ {0.expected}, got {0.actual}.",
        errors.FloatValueError: [
            (
                lambda error: error.expected == "finite" and error.actual < 0,
                "Expected finite number, got -∞.",
            ),
            (
                lambda error: error.expected == "finite" and error.actual > 0,
                "Expected finite number, got +∞.",
            ),
            (lambda error: error.expected == "number", "Expected number, got NaN."),
        ],
        errors.StrDecodeError: "Cannot decode value using “{0.expected}” encoding.",
        errors.MinLengthError: "Expected value length ≥ {0.expected}, got {0.actual}.",
        errors.MaxLengthError: "Expected value length ≤ {0.expected}, got {0.actual}.",
        errors.TupleLengthError: [
            (
                lambda error: error.expected == 1,
                "Expected exactly 1 element, got {0.actual}.",
            ),
            "Expected exactly {0.expected} elements, got {0.actual}.",
        ],
        errors.PatternMatchError: "Cannot match “{0.actual}” using “{0.expected}”.",
        errors.DatetimeParseError: [
            (
                lambda error: isinstance(error.expected, str),
                "Cannot parse date/time value from “{0.actual}” using “{0.expected}” format.",
            ),
            "Cannot parse date/time value from “{0.actual}”.",
        ],
        errors.DatetimeTypeError: [
            (
                lambda error: error.expected == "naive",
                "Naive date/time object is expected.",
            ),
            (
                lambda error: error.expected == "tzaware",
                "Timezone-aware date/time object is expected.",
            ),
        ],
        errors.RecursionMaxDepthError: (
            "Too many nested structures, limit is {0.expected}."
        ),
        errors.ForbiddenKeyError: "Key is not allowed.",
        errors.MissingKeyError: "Required key is not provided.",
    }
)
