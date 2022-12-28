envdev:
	python3.9 -m venv envdev
	envdev/bin/pip install -r requirements/all.txt
	envdev/bin/pip install -e .

# -----------------------------------------------------------------------------

check: envdev
	envdev/bin/python3 setup.py build_ext --inplace
	envdev/bin/pytest --flakes validx
	envdev/bin/mypy --implicit-optional validx
	envdev/bin/mypy --implicit-optional tests/typechecking

unittests: T = tests/unittests
unittests: envdev
	envdev/bin/python3 setup.py build_ext --inplace
	envdev/bin/pytest -c tests/unittests.ini $(T)

benchmarks: envdev
	envdev/bin/python3 setup.py build_ext --inplace
	envdev/bin/pytest -c tests/benchmarks.ini tests/benchmarks

.PHONY: docs
docs: envdev
	mkdir -p docs/_build
	envdev/bin/sphinx-build -W -b doctest docs docs/_build
	envdev/bin/sphinx-build -W -b html docs docs/_build
	envdev/bin/pyroma -d .

matrixtests: envdev clean-src
	envdev/bin/tox

# -----------------------------------------------------------------------------

clean-env:
	rm -rf .tox
	rm -rf envdev

clean-build:
	rm -rf dist
	rm -rf build
	rm -rf ValidX.egg-info
	rm -rf tests/build
	rm -rf tests/ValidX.egg-info

clean-src:
	find ./validx -name '*.c' -delete
	find ./validx -name '*.so' -delete

clean-docs:
	rm -rf docs/_build

clean-cache:
	rm -rf .mypy_cache
	rm -rf .benchmarks
	rm -rf .coverage
	rm -rf tests/.benchmarks
	rm -rf tests/.coverage

clean-all: clean-env clean-build clean-src clean-docs clean-cache
