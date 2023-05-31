.. _benchmarks:

Benchmarks
==========

ValidX is the fastest validation library among the following competitors.

*   `Cerberus 1.3.4 <http://docs.python-cerberus.org/en/stable/>`_ ~145x slower
*   `Colander 2.0 <https://docs.pylonsproject.org/projects/colander/en/latest/>`_ ~3x slower
*   `JSONSchema 4.17.3 <https://python-jsonschema.readthedocs.io/en/latest/>`_ ~20x slower
*   `Marshmallow 3.19.0 <https://marshmallow.readthedocs.io/en/stable/>`_ ~14x slower
*   `Pydantic 1.10.8 <https://docs.pydantic.dev/1.10/>`_ ~5x slower
*   `Schema 0.7.5 <https://github.com/keleshev/schema>`_  ~30x slower
*   `Voluptuous 0.13.1 <http://alecthomas.github.io/voluptuous/docs/_build/html/index.html>`_ ~3.5x slower


The following competitors have been excluded from the benchmark,
because the libraries do not work on Python >= 3.10.

*   `Valideer 0.4.2 <https://github.com/podio/valideer>`_
    had compatible performance with pure-Python implementation of ValidX.
    Excluded until `issue #27 <https://github.com/podio/valideer/issues/27>`_ is fixed.
*   `Validr 1.2.1 <https://github.com/guyskk/validr>`_
    had compatible performance with Cython implementation of ValidX.
    Excluded until `issue #60 <https://github.com/guyskk/validr/issues/60>`_ is fixed.

Use the following command to run benchmarks::

    make benchmarks

I got the following results on my laptop:

*   CPU Intel i7-1260P
*   RAM 32GB
*   OS Xubuntu 22.04.2, Linux core 5.15.0-72-generic
*   Python 3.10.6

::

    ----------------------------------------------------- benchmark: 9 tests -----------------------------------------------------
    Name (time in us)          Min                   Max                Mean              StdDev            OPS (Kops/s)
    ------------------------------------------------------------------------------------------------------------------------------
    test_validx_cy          1.8540 (1.0)          6.6900 (1.0)        2.0220 (1.0)        0.1247 (1.0)          494.5673 (1.0)
    test_validx_py          3.5870 (1.93)        11.1630 (1.67)       4.0128 (1.98)       0.2350 (1.88)         249.2040 (0.50)
    test_colander           5.9800 (3.23)        19.6410 (2.94)       6.6070 (3.27)       0.3332 (2.67)         151.3540 (0.31)
    test_voluptuous         7.0590 (3.81)        18.3420 (2.74)       7.6800 (3.80)       0.3089 (2.48)         130.2080 (0.26)
    test_pydantic           8.7520 (4.72)        23.0670 (3.45)      10.5461 (5.22)       0.5650 (4.53)          94.8216 (0.19)
    test_marshmallow       26.5630 (14.33)       47.8270 (7.15)      28.7742 (14.23)      0.9160 (7.34)          34.7533 (0.07)
    test_jsonschema        44.2580 (23.87)       62.9430 (9.41)      47.4968 (23.49)      1.3421 (10.76)         21.0540 (0.04)
    test_schema            61.0670 (32.94)       82.3220 (12.31)     65.3104 (32.30)      1.5263 (12.24)         15.3115 (0.03)
    test_cerberus         250.4110 (135.07)   6,304.0850 (942.31)   295.1710 (145.98)   207.4218 (>1000.0)        3.3879 (0.01)
    ------------------------------------------------------------------------------------------------------------------------------


Why you should care about performance
-------------------------------------

..  note::

    I got tired to update the numbers in this section on each release.
    So I decided to give up.
    Let it be as it is.
    The numbers here are outdated and not based on the benchmark above anymore.
    But it doesn't change the main point —
    performance is important.

I have been asked by my colleagues:
“Why should we care about performance?
Data validation is not a bottleneck usually.”
And it is correct.
But let's look on it from other side.

Let's say you have a web application that uses Cerberus for data validation,
because Cerberus is the number one in `7 Best Python Libraries for Validating Data`_.
How much will you earn replacing Cerberus by ValidX?

According to the benchmark above Cerberus spends 808 μs for each request,
while ValidX only 2 μs.
So that you will save 806 μs for each request.
How much is it?

If you have a small webserver that takes about 200 requests per second
(I took the number from this `discussion on Stack Overflow`_),
you will save::

    806 μs × 200 × 60 × 60 × 24 = 13927.68 s/day
    13927.68 ÷ 60 ÷ 60 = 3.8688 h/day

Yes,
you will save almost 4 hours of server time daily,
or almost 5 days monthly!
It is about $5 monthly for each general purpose ``t3.medium`` instance on AWS_,
which costs $0.0416 per hour.

And now it is time to look at your logs,
calculate number of requests you got in the last month,
and compare it with a bill from your hosting provider.

.. _7 Best Python Libraries for Validating Data: https://www.yeahhub.com/7-best-python-libraries-validating-data/
.. _discussion on Stack Overflow: https://stackoverflow.com/questions/1319965/how-many-requests-per-minute-are-considered-heavy-load-approximation
.. _AWS: https://aws.amazon.com/ec2/pricing/on-demand/
