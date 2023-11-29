from unittest import TestCase

from tracelogger import tracelogger


@tracelogger
def second_test_function(x):
    y = x**2
    return y


@tracelogger()
def first_test_function(a, b):
    c = a + b
    for k in range(5):
        if k % 2 == 0:
            b += k
        else:
            c += k
            second_test_function(c)
    return a, b, c


class TestTracelogger(TestCase):
    def test_tracelogger(self):
        a, b, c = first_test_function(a=10, b=20)
        self.assertEqual(a, 10)
        self.assertEqual(b, 26)
        self.assertEqual(c, 34)
