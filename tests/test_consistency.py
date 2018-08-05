import inspect
import os

import pytest

import validateit
from validateit import py, cy


DEV_MODE = os.environ.get("VALIDATEIT_DEV", False)


@pytest.mark.skipif(not DEV_MODE, reason="Development mode test")
def test_public_names(module):
    for name in module.__all__:
        assert name in validateit.__all__

        obj = getattr(module, name)

        if inspect.isclass(obj) and not name == "Validator":
            assert module.classes.get(name) is obj
            assert issubclass(obj, module.Validator)


@pytest.mark.skipif(not DEV_MODE, reason="Development mode test")
def test_interfaces():
    assert py.__all__ == cy.__all__

    py_root = os.path.dirname(os.path.abspath(py.__file__))
    cy_root = os.path.dirname(os.path.abspath(cy.__file__))

    for filename in os.listdir(py_root):
        if not filename.endswith(".pyi"):
            continue
        py_filename = os.path.join(py_root, filename)
        cy_filename = os.path.join(cy_root, filename)
        with open(py_filename) as py_file:
            with open(cy_filename) as cy_file:
                assert py_file.read() == cy_file.read()


@pytest.mark.skipif(not DEV_MODE, reason="Development mode test")
def test_docstrings():
    def walk(py_obj, cy_obj):
        for name in getattr(py_obj, "__all__", dir(py_obj)):
            if name.startswith("_"):
                continue

            py_attr = getattr(py_obj, name)
            if not (
                inspect.ismodule(py_attr)
                or inspect.isclass(py_attr)
                or inspect.ismethod(py_attr)
                or inspect.isfunction(py_attr)
            ):
                continue

            cy_attr = getattr(cy_obj, name)
            assert py_attr.__doc__ == cy_attr.__doc__

            if inspect.ismodule(py_attr) or inspect.isclass(py_attr):
                walk(py_attr, cy_attr)

    walk(py, cy)
