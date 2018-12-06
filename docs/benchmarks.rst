.. _benchmarks:

Benchmarks
==========

ValidX is the fastest validation library among the following competitors:

*   `Cerberus 1.2 <http://docs.python-cerberus.org/en/stable/>`_ ~400x slower
*   `Colander 1.5.1 <https://docs.pylonsproject.org/projects/colander/en/latest/>`_ ~10x slower
*   `JSONSchema 2.6.0 <https://python-jsonschema.readthedocs.io/en/latest/>`_ ~25x slower
*   `Schema 0.6.8 <https://github.com/keleshev/schema>`_ ~72x slower
*   `Valideer 0.4.2 <https://github.com/podio/valideer>`_ ~7.5x slower
*   `Voluptuous 0.11.5 <http://alecthomas.github.io/voluptuous/docs/_build/html/index.html>`_ ~10x slower
*   `Validr 1.0.6 <https://github.com/guyskk/validr>`_ ~2.5x slower
*   `Marshmallow 2.16.3 <https://marshmallow.readthedocs.io/en/stable/>`_ ~10x slower

Use the following command to run benchmarks::

    tox -ebm

I got the following results on my laptop:

*   CPU Intel i5-5200U 2.20GHz
*   RAM 8GB
*   OS Xubuntu 18.04, Linux core 4.15.0-42-generic
*   Python 3.7.1

::

    ----------------------------------------------------- benchmark: 10 tests -----------------------------------------------------
    Name (time in us)          Min                    Max                Mean              StdDev            OPS (Kops/s)
    -------------------------------------------------------------------------------------------------------------------------------
    test_validx_cy          1.8870 (1.0)          20.6430 (1.0)        1.9858 (1.0)        0.3867 (1.0)          503.5804 (1.0)
    test_validr             4.7860 (2.54)         34.9850 (1.69)       5.2407 (2.64)       1.0678 (2.76)         190.8137 (0.38)
    test_validx_py         10.4140 (5.52)         41.3780 (2.00)      10.7922 (5.43)       1.1939 (3.09)          92.6595 (0.18)
    test_valideer          14.7040 (7.79)         48.3870 (2.34)      15.2404 (7.67)       1.3992 (3.62)          65.6152 (0.13)
    test_marshmallow       18.8690 (10.00)        52.8380 (2.56)      19.8564 (10.00)      1.8984 (4.91)          50.3616 (0.10)
    test_voluptuous        19.6240 (10.40)        75.6600 (3.67)      20.3108 (10.23)      1.6403 (4.24)          49.2348 (0.10)
    test_colander          19.7640 (10.47)        65.6900 (3.18)      20.6069 (10.38)      2.3832 (6.16)          48.5274 (0.10)
    test_jsonschema        48.5700 (25.74)       135.6330 (6.57)      50.7647 (25.56)      6.5271 (16.88)         19.6987 (0.04)
    test_schema           140.4190 (74.41)       327.6610 (15.87)    143.9490 (72.49)      7.1405 (18.47)          6.9469 (0.01)
    test_cerberus         763.2160 (404.46)   11,055.2380 (535.54)   834.3364 (420.16)   581.7410 (>1000.0)        1.1986 (0.00)
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

According to the benchmark above Cerberus spends 834 μs for each request,
while ValidX only 2 μs.
So that you will save 832 μs for each request.
How much is it?

If you have a small webserver that takes about 200 requests per second
(I took the number from this `discussion on Stack Overflow`_),
you will save::

    832 μs × 200 × 60 × 60 × 24 = 14376.96 s/day
    14376.96 ÷ 60 ÷ 60 = 3.9936 h/day

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
