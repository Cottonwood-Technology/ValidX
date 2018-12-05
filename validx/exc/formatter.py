# coding: utf-8

import sys

from . import errors

if sys.version_info[0] < 3:  # pragma: no cover
    string = basestring  # noqa
else:  # pragma: no cover
    string = str


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
            assert isinstance(template, (string, list, tuple)), template
            if isinstance(template, (list, tuple)):
                for f in template:
                    assert isinstance(f, (string, tuple))
                    if isinstance(f, tuple):
                        assert len(f) == 2, f
                        assert callable(f[0]), f[0]
                        assert isinstance(f[1], string), f[1]
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
            elif isinstance(template, string):
                result.append((context, template.format(e)))
            elif isinstance(template, (list, tuple)):
                for f in template:
                    if isinstance(f, tuple) and f[0](e):
                        result.append((context, f[1].format(e)))
                        break
                    elif isinstance(f, string):
                        result.append((context, f.format(e)))
                        break
                else:
                    result.append((context, e.format_error()))
        return result


format_error = Formatter(
    {
        errors.InvalidTypeError: [
            (lambda error: error.actual is type(None), u"Value should not be null."),
            u"Expected type “{0.expected.__name__}”, got “{0.actual.__name__}”.",
        ],
        errors.OptionsError: [
            (
                lambda error: len(error.expected) == 1,
                u"Expected {0.expected[0]}, got {0.actual}.",
            ),
            u"Expected one of {0.expected}, got {0.actual}.",
        ],
        errors.MinValueError: u"Expected value ≥ {0.expected}, got {0.actual}.",
        errors.MaxValueError: u"Expected value ≤ {0.expected}, got {0.actual}.",
        errors.FloatValueError: [
            (
                lambda error: error.expected == "finite" and error.actual < 0,
                u"Expected finite number, got -∞.",
            ),
            (
                lambda error: error.expected == "finite" and error.actual > 0,
                u"Expected finite number, got +∞.",
            ),
            (lambda error: error.expected == "number", u"Expected number, got NaN."),
        ],
        errors.StrDecodeError: u"Cannot decode value using “{0.expected}” encoding.",
        errors.MinLengthError: u"Expected value length ≥ {0.expected}, got {0.actual}.",
        errors.MaxLengthError: u"Expected value length ≤ {0.expected}, got {0.actual}.",
        errors.TupleLengthError: [
            (
                lambda error: error.expected == 1,
                u"Expected exactly 1 element, got {0.actual}.",
            ),
            u"Expected exactly {0.expected} elements, got {0.actual}.",
        ],
        errors.PatternMatchError: u"Cannot match “{0.actual}” using “{0.expected}”.",
        errors.DatetimeParseError: [
            (
                lambda error: isinstance(error.expected, string),
                u"Cannot parse date/time value from “{0.actual}” using “{0.expected}” format.",
            ),
            u"Cannot parse date/time value from “{0.actual}”.",
        ],
        errors.DatetimeTypeError: [
            (
                lambda error: error.expected == "naive",
                u"Naive date/time object is expected.",
            ),
            (
                lambda error: error.expected == "tzaware",
                u"Timezone-aware date/time object is expected.",
            ),
        ],
        errors.RecursionMaxDepthError: (
            u"Too many nested structures, limit is {0.expected}."
        ),
        errors.ForbiddenKeyError: u"Key is not allowed.",
        errors.MissingKeyError: u"Required key is not provided.",
    }
)
