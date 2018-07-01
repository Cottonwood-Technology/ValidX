from setuptools import setup, find_packages


ext_modules = []
requirements = []

try:
    from Cython.Build import cythonize
except ImportError:
    pass
else:
    directives = {}
    ext_modules = cythonize("validateit/cy/*.pyx", compiler_directives=directives)

with open("README.rst") as f:
    readme = f.read()

setup(
    name="ValidateIt",
    version="0.1",
    description="TODO",
    long_description=readme,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="validator validation validate schema",
    url="http://www.cottonwood.tech",
    author="Cottonwood Technology",
    author_email="info@cottonwood.tech",
    license="BSD",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    ext_modules=ext_modules,
    install_requires=requirements,
)
