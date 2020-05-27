.. _benchmarks:

Benchmarks
==========

When ValidX had been released,
it was the fastest validation library among the following competitors.
It isn't true anymore.
However,
it would be unfair to remove this section from the documentation.
Once the challenge has been thrown down,
the competition must go on.

*   `Cerberus 1.3.2 <http://docs.python-cerberus.org/en/stable/>`_ ~130x slower
*   `Colander 1.7.0 <https://docs.pylonsproject.org/projects/colander/en/latest/>`_ ~2.8x slower
*   `JSONSchema 3.2.0 <https://python-jsonschema.readthedocs.io/en/latest/>`_ ~11x slower
*   `Marshmallow 3.6.0 <https://marshmallow.readthedocs.io/en/stable/>`_ ~11x slower
*   `Schema 0.7.2 <https://github.com/keleshev/schema>`_  ~29x slower
*   `Valideer 0.4.2 <https://github.com/podio/valideer>`_ ~2x slower,
    but it has compatible performance with pure-Python implementation of ValidX.
    In some rounds it is a bit faster,
    in other is a bit slower.
*   `Validr 1.2.0 <https://github.com/guyskk/validr>`_
    has compatible performance with Cython implementation of ValidX.
    In some rounds it is a bit faster,
    in other is a bit slower.
*   `Voluptuous 0.11.7 <http://alecthomas.github.io/voluptuous/docs/_build/html/index.html>`_ ~3x slower

Use the following command to run benchmarks::

    tox -ebm

I got the following results on my laptop:

*   CPU Intel i5-5200U 2.20GHz
*   RAM 8GB
*   OS Xubuntu 18.04, Linux core 4.15.0-101-generic
*   Python 3.8.2

::

    ----------------------------------------------------- benchmark: 10 tests -----------------------------------------------------
    Name (time in us)          Min                    Max                Mean              StdDev            OPS (Kops/s)
    -------------------------------------------------------------------------------------------------------------------------------
    test_validx_cy          5.8240 (1.0)          41.5310 (1.0)        6.1031 (1.0)        0.9631 (1.0)          163.8516 (1.0)
    test_validr             6.6680 (1.14)        191.4440 (4.61)       7.0912 (1.16)       1.7589 (1.83)         141.0205 (0.86)
    test_validx_py         12.1390 (2.08)         63.1280 (1.52)      12.5840 (2.06)       1.5104 (1.57)          79.4661 (0.48)
    test_valideer          12.9530 (2.22)        101.5800 (2.45)      13.4117 (2.20)       1.4033 (1.46)          74.5618 (0.46)
    test_colander          16.6500 (2.86)         94.6480 (2.28)      17.3843 (2.85)       2.1166 (2.20)          57.5232 (0.35)
    test_voluptuous        18.4060 (3.16)         69.2420 (1.67)      19.2751 (3.16)       2.3339 (2.42)          51.8804 (0.32)
    test_marshmallow       67.0080 (11.51)       291.5290 (7.02)      69.9401 (11.46)      8.1468 (8.46)          14.2980 (0.09)
    test_jsonschema        70.4520 (12.10)       242.8030 (5.85)      73.0181 (11.96)      7.5669 (7.86)          13.6952 (0.08)
    test_schema           171.8870 (29.51)       332.5750 (8.01)     177.0150 (29.00)     10.8829 (11.30)          5.6492 (0.03)
    test_cerberus         725.5970 (124.59)   11,228.9250 (270.37)   801.7096 (131.36)   561.3559 (582.86)         1.2473 (0.01)
    -------------------------------------------------------------------------------------------------------------------------------



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
