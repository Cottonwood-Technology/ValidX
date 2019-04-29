.. _usage:

Usage
=====

Installation
------------

The library is shipped with two interchangeable parts:
pure Python and optimized Cython_ versions.
In the most cases,
you will get a ready to use binary wheel during installation from PyPI_.

..  code-block:: shell

    pip install validx

However,
if it fails to find a wheel compatible with your OS,
it will try to install source code tarball and compile it on the fly.
To get the optimized version,
you have to have Cython
(in addition to C/C++ compiler and Python header files)
installed **before** ValidX installation.
If it fails to import Cython during setup,
no compilation will be done.
And you will get the pure Python version of the library.

You can check which version has been installed using the following code:

..  code-block:: pycon

    >>> import validx
    >>> validx.__impl__
    'Cython'

.. _PyPI: https://pypi.org/
.. _Cython: http://cython.org/


.. _usage-quick-start:

Quick Start
-----------

Let's build a simple validator for some web-application endpoint,
which performs full-text search with optional filtering by tags:

..  testcode:: quick_start

    from validx import Dict, List, Str, Int

    search_params = Dict(
        {
            "query": Str(minlen=3, maxlen=500),    # Search query
            "tags": List(Str(pattern=r"^[\w]+$")), # Optional list of tags
            "limit": Int(min=0, max=100),          # Pagination parameters
            "offset": Int(min=0),
        },
        defaults={
            "limit": 100,
            "offset": 0,
        },
        optional=["tags"],
    )


And test it:

..  testcode:: quick_start

    assert search_params({"query": "Craft Beer"}) == {
        "query": "Craft Beer",
        "limit": 100,
        "offset": 0,
    }
    assert search_params({"query": "Craft Beer", "offset": 100}) == {
        "query": "Craft Beer",
        "limit": 100,
        "offset": 100,
    }
    assert search_params({"query": "Craft Beer", "tags": ["APA"]}) == {
        "query": "Craft Beer",
        "tags": ["APA"],
        "limit": 100,
        "offset": 0,
    }

See :ref:`reference` for complete list of available validators and their parameters.


Error Handling
--------------

Each validator tries to handle as much as possible.
It means,
a result exception raised by the validator may contain many errors.

..  testcode:: quick_start

    from validx import exc

    try:
        search_params({"limit": 200})
    except exc.ValidationError as e:
        error = e

    error.sort()
    print(error)

..  testoutput:: quick_start

    <SchemaError(errors=[
        <limit: MaxValueError(expected=100, actual=200)>,
        <query: MissingKeyError()>
    ])>

As you can see,
the result exception ``error`` has type :class:`validx.exc.SchemaError`,
which contains two errors:
:class:`validx.exc.MaxValueError` and :class:`validx.exc.MissingKeyError`.

To unify error handling,
each exception provides Sequence interface.
It means,
you can iterate them,
get by index and sort nested errors.

..  testcode:: quick_start

    # SchemaError iteration is done over its nested errors
    for suberror in error:
        print(suberror)

..  testoutput:: quick_start

    <limit: MaxValueError(expected=100, actual=200)>
    <query: MissingKeyError()>

..  testcode:: quick_start

    # Error of other class just yields itself during iteration
    for suberror in error[0]:
        print(suberror)

..  testoutput:: quick_start

    <limit: MaxValueError(expected=100, actual=200)>

Take a note on calling ``error.sort()`` before printing the error.
It sorts nested errors by their contexts.

Context is a full path to the failed member of validated structure.
For example,
let's add an ``order`` parameter to the ``search_params`` schema,
which accepts list of tuples ``[(field_name, sort_direction), ...]``:

..  testcode:: error_context

    from validx import exc, Dict, List, Tuple, Str, Int

    search_params = Dict(
        {
            "query": Str(minlen=3, maxlen=500),
            "tags": List(Str(pattern=r"^[\w]+$")),
            "limit": Int(min=0, max=100),
            "offset": Int(min=0),
            "order": List(
                Tuple(
                    Str(options=["name", "added"]),  # Field name
                    Str(options=["asc", "desc"]),    # Sort direction
                ),
            ),
        },
        defaults={
            "limit": 100,
            "offset": 0,
            "order": [("added", "desc")],
        },
        optional=["tags"],
    )


And pass invalid value into it:

..  testcode:: error_context

    try:
        search_params({
            "query": "Craft Beer",
            "order": [("name", "ascending"), ("description", "asc")],
        })
    except exc.ValidationError as e:
        error = e

    error.sort()
    print(error)

..  testoutput:: error_context

    <SchemaError(errors=[
        <order.0.1: OptionsError(expected=['asc', 'desc'], actual='ascending')>,
        <order.1.0: OptionsError(expected=['name', 'added'], actual='description')>
    ])>

Take a note on contexts,
for example ``order.0.1``.
It means,
that the error has occurred at ``order`` dictionary key,
at the first element of the list (index ``0``),
and at the second element of the tuple (index ``1``).

Technically error context is a deque,
so it can be easily inspected:

..  testcode:: error_context

    print(error[0].context)

..  testoutput:: error_context

    deque(['order', 0, 1])

The library also provides special context markers,
to distinguish special cases
(such as failed pipeline steps)
from dictionary keys and list/tuple indexes.
See :ref:`reference-context-markers` section for details.

There is also :ref:`reference-error-formatter`,
that returns a human friendly error messages.

..  testcode:: error_context

    try:
        search_params({"limit": 200})
    except exc.ValidationError as e:
        for context, message in exc.format_error(e):
            print("%s: %s" % (context, message))

..  testoutput:: error_context

    limit: Expected value ≤ 100, got 200.
    query: Required key is not provided.

It is probably not what you want.
It does not provide any localization,
for instance,
but you can look over its sources and figure out how to build your own one.
So its purpose is mostly to be an example rather than a useful tool.


Reusable Validators
-------------------

There is a quite common task to create a bunch of basic validators in a project,
and then build complex ones from them.

For example,
you have validators for handling resource IDs and names:

..  testcode:: reusable_validators_1

    from validx import Int, Str

    resource_id = Int(min=1)
    resource_name = Str(minlen=1, maxlen=200)

You can use them directly in a complex validator,
because they work as pure functions and produce no side effects during validation.

..  testcode:: reusable_validators_1

    from validx import Dict

    resource_update_params = Dict({
        "id": resource_id,
        "name": resource_name,
    })


..  warning::

    There is only one validator that does not work as pure function —
    :class:`validx.py.LazyRef`.
    See :ref:`usage-recursive-structure-validation` section for details.

However,
importing each basic validator might be tedious.
So you can use :ref:`reference-instance-registry` provided by the library.

..  testcode:: reusable_validators_2

    from validx import instances, Int, Str, Dict

    Int(alias="resource_id", min=1)
    Str(alias="resource_name", minlen=1, maxlen=200)

    resource_update_params = Dict({
        "id": instances.get("resource_id"),
        "name": instances.get("resource_name"),
    })

..  testcleanup:: reusable_validators_2

    instances.clear()


Cloning Validators
------------------

There is another common task to create a new validator,
based on existent one with slightly different parameters.
You can use cloning for such purpose.

Cloning might look a bit tricky,
so here is the list of examples,
that covers the most possible use cases.

Example 1.
Create a validator adding constraint to base one.

..  testcode:: cloning_validators_1

    from validx import Int

    resource_id = Int(min=1)
    nullable_resource_id = resource_id.clone(
        update={
            "/": {"nullable": True},
        },
    )

    print(resource_id)
    print(nullable_resource_id)

..  testoutput:: cloning_validators_1

    <Int(min=1)>
    <Int(nullable=True, min=1)>

Example 2.
Create a validator removing constraint from base one.

..  testcode:: cloning_validators_2

    from validx import Int

    nullable_resource_id = Int(min=1, nullable=True)
    resource_id = nullable_resource_id.clone(
        unset={
            "/": ["nullable"],
        },
    )

    print(nullable_resource_id)
    print(resource_id)

..  testoutput:: cloning_validators_2

    <Int(nullable=True, min=1)>
    <Int(min=1)>

Example 3.
Create a validator updating constraint of base one.

..  testcode:: cloning_validators_3

    from validx import Str

    resource_action = Str(options=("create", "update", "read", "delete"))
    email_action = resource_action.clone(
        unset={
            "/options": [1],  # Remove second element ``update``
        },
        update={
            "/options": {"extend": ["spam", "archive"]},
        },
    )

    print(resource_action)
    print(email_action)

..  testoutput:: cloning_validators_3

    <Str(options=('create', 'update', 'read', 'delete'))>
    <Str(options=('create', 'read', 'delete', 'spam', 'archive'))>

Example 4.
Create a validator updating constraint of nested validator of base one.

..  testcode:: cloning_validators_4

    from validx import Tuple, Str

    resource_order = Tuple(
        Str(options=("name", "added")),  # Field name
        Str(options=("asc", "desc")),    # Sort direction
    )
    article_order = resource_order.clone(
        update={
            "/items/0/options": {0: "title"},
        },
    )
    search_order = resource_order.clone(
        update={
            "/items/0/options": {"extend": ["relevance"]},
        },
    )

    print(resource_order)
    print(article_order)
    print(search_order)

..  testoutput:: cloning_validators_4

    <Tuple(items=(<Str(options=('name', 'added'))>, <Str(options=('asc', 'desc'))>))>
    <Tuple(items=(<Str(options=('title', 'added'))>, <Str(options=('asc', 'desc'))>))>
    <Tuple(items=(<Str(options=('name', 'added', 'relevance'))>, <Str(options=('asc', 'desc'))>))>

In a nutshell,
method :meth:`validx.py.Validator.clone`
accepts two arguments ``update`` and ``unset`` in the following format:

..  code-block:: python

    update = {
        "/path/to/element": {
            "dict_key|list_or_tuple_index|validator_parameter_name": "new value",
            ...
        },
        ...
    }

    unset = {
        "/path/to/element": [
            "dict_key|list_or_tuple_index|validator_parameter_name",
            ...
        ],
        ...
    }


Dumping & Loading Validators
----------------------------

Each validator can be dumped into a dictionary and loaded from such dictionary.
It might be useful to serialize validators into JSON or load them from configuration.

..  testcode:: dumping_and_loading_validators

    from pprint import pprint
    from validx import Validator, Int

    resource_id = Int(min=1)
    dumped = resource_id.dump()

    pprint(dumped)
    print(Validator.load(dumped))

..  testoutput:: dumping_and_loading_validators

    {'__class__': 'Int', 'min': 1}
    <Int(min=1)>

You can register validators using aliases,
and use them or clone them later during loading process.

..  testcode:: dumping_and_loading_validators

    print(
        Validator.load({
            "__class__": "Int",
            "alias": "resource_id",
            "min": 1,
        })
    )
    print(
        Validator.load({
            "__clone__": "resource_id",
            "update": {
                "/": {
                    "alias": "nullable_resource_id",
                    "nullable": True,
                },
            },
        })
    )
    print(Validator.load({"__use__": "nullable_resource_id"}))

..  testoutput:: dumping_and_loading_validators

    <Int(min=1)>
    <Int(nullable=True, min=1)>
    <Int(nullable=True, min=1)>

..  testcleanup:: dumping_and_loading_validators

    from validx import instances
    instances.clear()


MultiDict Validation
--------------------

Popular web-frameworks parse ``application/x-www-form-urlencoded`` data
into so-called ``MultiDict`` structures.
There is no standard interface,
but implementations more or less compatible.
The main purpose of the structure is to pass arrays using key-value pairs,
where values with the same key are grouped into an array.

The search query from :ref:`usage-quick-start` section can look like this:

..  code-block:: http

    GET /catalog/search?query=Craft+Beer&tags=APA&tags=IPA HTTP/1.1

Let's rewrite the validator to handle such query:

..  code-block:: python

    from validx import Dict, List, Str, Int

    search_params = Dict(
        {
            "query": Str(minlen=3, maxlen=500),
            "tags": List(Str(pattern=r"^[\w]+$")),
            "limit": Int(min=0, max=100, coerce=True), # Coerce ``str`` to ``int``
            "offset": Int(min=0, coerce=True),
        },
        defaults={
            "limit": 100,
            "offset": 0,
        },
        optional=["tags"],
        multikeys=["tags"],  # Handle ``tags`` as a sequence
    )

And it can be used like this:

..  code-block:: python3

    # AIOHTTP request handler
    async def catalog_search(request):
        params = search_schema(request.url.query)
        # params == {
        #     "query": "Craft Beer",
        #     "tags": ["APA", "IPA"],
        #     "limit": 0,
        #     "offset": 0,
        # }
        ...

ValidX has been tested against the following implementations of ``MultiDict``:

*   `WebOb MultiDict`_;
*   `Werkzeug MultiDict`_;
*   `MultiDict`_ (that has been extracted from AIOHTTP_).

.. _WebOb MultiDict: https://docs.pylonsproject.org/projects/webob/en/stable/api/multidict.html#webob.multidict.MultiDict
.. _Werkzeug MultiDict: http://werkzeug.pocoo.org/docs/0.14/datastructures/#werkzeug.datastructures.MultiDict
.. _MultiDict: https://multidict.readthedocs.io/en/stable/
.. _AIOHTTP: https://aiohttp.readthedocs.io/en/stable/


Multiple-Step Validation
------------------------

Sometimes you need to split up validation process into several steps.
Prevalidate some common structure on the first one,
and make final validation on the latter one.

For example,
here is the schema for validation of `JSON-RPC 2.0`_ request:

..  testcode:: multiple_step

    from validx import Dict, Int, Str, Const, OneOf, Any

    jsonrpc = Dict(
        {
            "jsonrpc": Const("2.0"),
            "id": OneOf(
                Int(nullable=True),
                Str(minlen=1, maxlen=100),
            ),
            "method": Str(minlen=1, maxlen=100),
            "params": Any(),
        },
        optional=("id", "params"),
    )


Take note of :class:`validx.py.Any` usage.
It accepts literally any value,
just like as we need here,
because parameters of concrete method will be validated on the next step.

..  testcode:: multiple_step

    login_params = Dict({
        "username": Str(minlen=1, maxlen=100),
        "password": Str(minlen=1, maxlen=100),
    })

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "login",
        "params": {"username": "jdoe", "password": "qwerty"},
    }

    assert jsonrpc(request) == request
    assert login_params(request["params"]) == request["params"]


.. _JSON-RPC 2.0: https://www.jsonrpc.org/specification


.. _usage-recursive-structure-validation:

Recursive Structure Validation
------------------------------

Let's see a real-world example.
A web application accepts search query as JSON in the following notation:

..  code-block:: python

    {"<function>": ["<arg_1>", "<arg_2>", ...]}

Simple comparison function accepts only two arguments:
field name and some value to compare with.
For example:

..  code-block:: python

    {"eq": ["type", "whiskey"]}                  # type == "whiskey"
    {"ne": ["status", "out_of_stock"]}           # status != "out_of_stock"
    {"in": ["origin", ["Scotland", "Ireland"]]}  # origin in ["Scotland", "Ireland"]
    {"gt": ["age", 10]}                          # age > 10
    {"lt": ["age", 20]}                          # age < 20

And there is also compound functions,
that can combine simple and other compound ones.
For example:

..  code-block:: python

    # type == "whiskey" and age > 10 and age < 20
    {
        "and": [
            {"eq": ["type", "whiskey"]},
            {"gt": ["age", 10]},
            {"lt": ["age", 20]},
        ]
    }

There is obviously recursive validator needed.
Here is how it can be built:

..  testcode:: recursive_structure_validation

    from validx import Dict, List, Tuple, OneOf, Any, LazyRef, Str

    # Validator for simple function
    simple_query = Dict(
        extra=(
            # accept dict key as the following function names
            Str(options=("eq", "ne", "in", "lt", "gt")),

            # accept dict value as a tuple of two elements
            Tuple(
                Str(),  # field name
                Any(),  # parameter,
                        # that will be validated on the next step,
                        # taking into account type of specified field
                        # and comparison function
            ),
        ),
        minlen=1,  # at least one function should be specified
    )

    # Validator for compound function
    compound_query = Dict(
        extra=(
            # accept dict key as the following function names
            Str(options=("and", "or", "not")),

            # accept dict value as a list of other functions
            List(
                # make a lazy reference on ``query_dsl`` validator,
                # which is defined below,
                # and allow maximum 5 levels of recursion
                LazyRef("query_dsl", maxdepth=5)
            ),
        ),
        minlen=1,  # again, at least one function should be specified
    )

    # And the final validator
    query_dsl = OneOf(
        simple_query,
        compound_query,

        # register the validator under ``query_dsl`` alias,
        # so it will be accessible via ``LazyRef`` above
        alias="query_dsl",
    )

Here we use :class:`validx.py.LazyRef`
to create circular reference on the parent validator.
Each time it is called,
it increments its recursive call depth and checks the limit in the following.
If the limit is reached,
it raises :class:`validater.exc.RecursionMaxDepthError`.

..  warning::

    Be careful cloning such validators.
    You should register a clone using new alias,
    and also update ``use`` parameter of ``LazyRef`` to the same new alias.
    If you don't do this,
    you will definitely get some fun chasing a bunch of sneaky bugs.

Let's validate a sample query:

..  testcode:: recursive_structure_validation

    # (
    #   type == "whiskey"
    #   and origin in ["Scotland", "Ireland"]
    #   and age > 10
    #   and age < 20
    #   and status != "out_of_stock"
    # )
    query = {
        "and": [
            {"eq": ("type", "whiskey")},
            {"in": ("origin", ["Scotland", "Ireland"])},
            {"gt": ("age", 10)},
            {"lt": ("age", 20)},
            {"ne": ("status", "out_of_stock")},
        ],
    }
    assert query_dsl(query) == query

..  testcleanup:: recursive_structure_validation

    from validx import instances
    instances.clear()
