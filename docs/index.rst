.. ValidateIt documentation master file, created by
   sphinx-quickstart on Wed Aug  1 14:36:46 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ValidateIt
==========

ValidateIt is a fast, powerful, and flexible validator with sane syntax.

..  testcode::

    import validateit as v

    jsonrpc = v.Dict(
        {
            "jsonrpc": v.Const("2.0"),
            "id": v.OneOf(
                v.Int(nullable=True),
                v.Str(),
            ),
            "method": v.Str(),
            "params": v.OneOf(
                v.Dict(extra=(v.Str(), v.Any())),
                v.List(v.Any()),
            ),
        },
        optional=("id", "params"),
    )

    request = {
        "jsonrpc": "2.0",
        "method": "ping",
    }
    assert jsonrpc(request) == request

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "login",
        "params": {
            "username": "jdoe",
            "password": "qwerty"
        },
    }
    assert jsonrpc(request) == request

    request = {
        "jsonrpc": "2.0",
        "id": "48f5ebd0b9cff570162a61bed842ba2b",
        "method": "login",
        "params": ["jdoe", "qwerty"],
    }
    assert jsonrpc(request) == request


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
