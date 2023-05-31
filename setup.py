import os
import sys
import platform
from pathlib import Path

from setuptools import setup, find_packages


here = Path(__file__).parent
os.chdir(here)

ext_modules = []
requirements = []
package_data = []

if platform.python_implementation() == "CPython":
    try:
        from Cython.Build import cythonize
    except ImportError:
        print("Unable to import Cython. Pure Python version will be used.")
    else:
        ext_modules = cythonize(
            str(here / "validx/cy/*.pyx"),
            compiler_directives={"language_level": sys.version_info.major},
        )

with (here / "validx/__init__.py").open("r") as f:
    version = next(line for line in f if line.startswith("__version__"))
    version = version.strip().split(" = ")[1]
    version = version.strip('"')

with (here / "README.rst").open("r") as f:
    readme = f.read()

with (here / "CHANGES.rst").open("r") as f:
    changes = f.read()


src = here / "validx"
package_data.append("py.typed")
package_data.extend(str(p.relative_to(src)) for p in src.glob("**/*.pyi"))
package_data.extend(str(p.relative_to(src)) for p in src.glob("**/*.pyx"))
package_data.extend(str(p.relative_to(src)) for p in src.glob("**/*.pxd"))


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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires=">=3.6",
    keywords="validator validation validate schema",
    url="https://github.com/Cottonwood-Technology/ValidX",
    author="Cottonwood Technology",
    author_email="info@cottonwood.tech",
    license="BSD",
    packages=find_packages(where=str(here)),
    package_data={"validx": package_data},
    zip_safe=False,
    ext_modules=ext_modules,
    install_requires=requirements,
)
