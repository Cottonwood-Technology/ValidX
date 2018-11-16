.. ValidX documentation master file, created by
   sphinx-quickstart on Wed Aug  1 14:36:46 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ValidX
======

ValidX is :ref:`fast <benchmarks>`, powerful, and flexible validator with sane syntax.

..  testcode:: demo

    from validx import Dict, Str

    schema = Dict({"message": Str()})
    data = {"message": "ValidX is cool!"}

    print(schema(data))

..  testoutput:: demo

    {'message': 'ValidX is cool!'}


..  toctree::
    :maxdepth: 2
    :caption: Contents:

    usage
    reference
    benchmarks


Contribution
------------

The project sources are hosted on BitBucket_ as well,
as its bug tracker.
Pull requests,
bug reports,
and feedback are welcome.

.. _BitBucket: https://bitbucket.org/cottonwood-tech/validx/


License
-------

The code is licensed under the terms of BSD 2-Clause license.
The full text of the license can be found at the root of the sources.


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
