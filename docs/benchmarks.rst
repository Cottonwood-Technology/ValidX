.. _benchmarks:

Benchmarks
==========

ValidX is the fastest validation library among the following competitors:

*   `Cerberus <http://docs.python-cerberus.org/en/stable/>`_ ~400x slower
*   `Colander <https://docs.pylonsproject.org/projects/colander/en/latest/>`_ ~10x slower
*   `JSONSchema <https://python-jsonschema.readthedocs.io/en/latest/>`_ ~23.5x slower
*   `Schema <https://github.com/keleshev/schema>`_ ~72x slower
*   `Valideer <https://github.com/podio/valideer>`_ ~7.5x slower
*   `Voluptuous <http://alecthomas.github.io/voluptuous/docs/_build/html/index.html>`_ ~10x slower
*   `Validr <https://github.com/guyskk/validr>`_ ~2.5x slower

Use the following command to run benchmarks::

    tox -ebm

I got the following results on my laptop:

*   CPU Intel i5-5200U 2.20GHz
*   RAM 8GB
*   OS Xubuntu 16.04, Linux core 4.15.0-38-generic
*   Python 3.7.1

::

    ----------------------------------------------------- benchmark: 9 tests ------------------------------------------------------
    Name (time in us)          Min                    Max                Mean              StdDev            OPS (Kops/s)
    -------------------------------------------------------------------------------------------------------------------------------
    test_validx_cy          1.9470 (1.0)         131.1000 (2.51)       2.0616 (1.0)        0.6042 (1.0)          485.0534 (1.0)
    test_validr             4.8800 (2.51)        147.6810 (2.83)       5.0991 (2.47)       1.1789 (1.95)         196.1140 (0.40)
    test_validx_py         10.6050 (5.45)        125.1650 (2.40)      10.8890 (5.28)       1.4404 (2.38)          91.8356 (0.19)
    test_valideer          14.9070 (7.66)        166.7180 (3.20)      15.4275 (7.48)       1.8975 (3.14)          64.8193 (0.13)
    test_colander          19.9610 (10.25)        52.1790 (1.0)       20.7103 (10.05)      1.4433 (2.39)          48.2850 (0.10)
    test_voluptuous        20.1820 (10.37)       153.9890 (2.95)      20.8221 (10.10)      2.2893 (3.79)          48.0259 (0.10)
    test_jsonschema        47.2640 (24.28)       130.1100 (2.49)      48.7306 (23.64)      3.1049 (5.14)          20.5210 (0.04)
    test_schema           141.4300 (72.64)       351.3240 (6.73)     148.9070 (72.23)     21.5525 (35.67)          6.7156 (0.01)
    test_cerberus         766.0910 (393.47)   11,275.0520 (216.08)   834.1975 (404.63)   583.8028 (966.21)         1.1988 (0.00)
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
