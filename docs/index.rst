.. ValidateIt documentation master file, created by
   sphinx-quickstart on Wed Aug  1 14:36:46 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ValidateIt
==========

ValidateIt is fast, powerful, and flexible validator with sane syntax.

..  testcode:: demo

    from validateit import Dict, Str

    schema = Dict({"message": Str()})
    data = {"message": "ValidateIt is cool!"}

    print(schema(data))

..  testoutput:: demo

    {'message': 'ValidateIt is cool!'}


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   reference



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
