ValidateIt
==========

ValidateIt is fast_, powerful, and flexible validator with sane syntax.

..  code-block:: python

    from validateit import Dict, Str

    schema = Dict({"message": Str()})
    data = {"message": "ValidateIt is cool!"}

    print(schema(data))

::

    {'message': 'ValidateIt is cool!'}


The full documentation is available at `Read the Docs`_.

.. _fast: https://validateit.readthedocs.io/en/latest/benchmarks.html
.. _Read the Docs: https://validateit.readthedocs.io/en/latest/
