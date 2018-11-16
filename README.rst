
ValidX
======

ValidX is fast_, powerful, and flexible validator with sane syntax.

..  code-block:: python

    from validx import Dict, Str

    schema = Dict({"message": Str()})
    data = {"message": "ValidX is cool!"}

    print(schema(data))

::

    {'message': 'ValidX is cool!'}


The full documentation is available at `Read the Docs`_.

.. _fast: https://validx.readthedocs.io/en/latest/benchmarks.html
.. _Read the Docs: https://validx.readthedocs.io/en/latest/
