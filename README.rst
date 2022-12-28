
ValidX
======

..  image:: https://github.com/Cottonwood-Technology/ValidX/actions/workflows/main.yaml/badge.svg
    :target: https://github.com/Cottonwood-Technology/ValidX/actions/workflows/main.yaml

..  image:: https://badge.fury.io/py/ValidX.svg
    :target: https://badge.fury.io/py/ValidX

..  image:: https://readthedocs.org/projects/validx/badge/?version=latest
    :target: https://validx.readthedocs.io/en/latest/?badge=latest

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
