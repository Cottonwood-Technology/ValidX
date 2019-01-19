.. _benchmarks:

Benchmarks
==========

ValidX is the fastest validation library among the following competitors:

*   `Cerberus 1.2 <http://docs.python-cerberus.org/en/stable/>`_ ~400x slower
*   `Colander 1.5.1 <https://docs.pylonsproject.org/projects/colander/en/latest/>`_ ~10x slower
*   `JSONSchema 2.6.0 <https://python-jsonschema.readthedocs.io/en/latest/>`_ ~25x slower
*   `Marshmallow 2.18.0 <https://marshmallow.readthedocs.io/en/stable/>`_ ~10x slower
*   `Schema 0.6.8 <https://github.com/keleshev/schema>`_ ~80x slower
*   `Valideer 0.4.2 <https://github.com/podio/valideer>`_ ~8x slower
*   `Validr 1.0.6 <https://github.com/guyskk/validr>`_ ~2.5x slower
*   `Voluptuous 0.11.5 <http://alecthomas.github.io/voluptuous/docs/_build/html/index.html>`_ ~10x slower

Use the following command to run benchmarks::

    tox -ebm

I got the following results on my laptop:

*   CPU Intel i5-5200U 2.20GHz
*   RAM 8GB
*   OS Xubuntu 18.04, Linux core 4.15.0-43-generic
*   Python 3.7.1

::

    ----------------------------------------------------- benchmark: 10 tests -----------------------------------------------------
    Name (time in us)          Min                    Max                Mean              StdDev            OPS (Kops/s)
    -------------------------------------------------------------------------------------------------------------------------------
    test_validx_cy          1.8010 (1.0)         31.0580 (1.01)       1.9217 (1.0)       0.4642 (1.0)          520.3821 (1.0)
    test_validr             4.5810 (2.54)        30.7720 (1.0)        4.8280 (2.51)      0.9594 (2.07)         207.1235 (0.40)
    test_validx_py         10.9450 (6.08)        43.2970 (1.41)      11.4764 (5.97)      1.4594 (3.14)          87.1353 (0.17)
    test_valideer          14.3730 (7.98)        50.3890 (1.64)      15.6638 (8.15)      1.8038 (3.89)          63.8415 (0.12)
    test_marshmallow       18.6680 (10.37)       64.8940 (2.11)      19.8704 (10.34)     3.1400 (6.76)          50.3261 (0.10)
    test_colander          19.2220 (10.67)       63.8260 (2.07)      20.1110 (10.47)     2.5595 (5.51)          49.7240 (0.10)
    test_voluptuous        19.5440 (10.85)       74.2500 (2.41)      20.7694 (10.81)     2.2002 (4.74)          48.1477 (0.09)
    test_jsonschema        46.5160 (25.83)      123.6060 (4.02)      47.9933 (24.97)     4.2259 (9.10)          20.8362 (0.04)
    test_schema           140.9530 (78.26)      346.2140 (11.25)    152.5474 (79.38)    26.5019 (57.10)          6.5553 (0.01)
    test_cerberus         760.6310 (422.34)   2,226.9750 (72.37)    808.2582 (420.60)   90.4889 (194.95)         1.2372 (0.00)
    -------------------------------------------------------------------------------------------------------------------------------


Why you should care about performance
-------------------------------------

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
