ValidateIt
==========

ValidateIt is fast, powerful, and flexible validator with sane syntax.

..  code-block:: python

    from validateit import Dict, Str

    schema = Dict({"message": Str()})
    data = {"message": "ValidateIt is cool!"}

    print(schema(data))

::

    {'message': 'ValidateIt is cool!'}
