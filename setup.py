import sys
import platform

from setuptools import setup, find_packages


ext_modules = []
requirements = []

if platform.python_implementation() == "CPython":
    try:
        from Cython.Build import cythonize
    except ImportError:
        print("Unable to import Cython. Pure Python version will be used.")
    else:
        directives = {"language_level": sys.version_info[0]}
        ext_modules = cythonize("src/validx/cy/*.pyx", compiler_directives=directives)

with open("src/validx/__init__.py") as f:
    version = next(line for line in f if line.startswith("__version__"))
    version = version.strip().split(" = ")[1]
    version = version.strip('"')

with open("README.rst") as f:
    readme = f.read()

with open("CHANGES.rst") as f:
    changes = f.read()

setup(
    name="ValidX",
    version=version,
    description="fast, powerful, and flexible validator with sane syntax",
    long_description=readme + "\n\n" + changes,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="validator validation validate schema",
    url="https://github.com/Cottonwood-Technology/ValidX",
    author="Cottonwood Technology",
    author_email="info@cottonwood.tech",
    license="BSD",
    package_dir={"validx": "src/validx"},
    packages=find_packages(where="src"),
    package_data={"": ["*.pyi"], "validx": ["py.typed"]},
    zip_safe=False,
    ext_modules=ext_modules,
    install_requires=requirements,
)
