from unittest import TestCase

from tracelogger import multiline_printer, names_printer, tracelogger


@tracelogger
def second_test_function(x):
    y = x**2
    return y


@tracelogger(printer=lambda locals_: names_printer(locals_=locals_, names=['k', 'b']))
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

    def test_multiline_printer_with_custom_width(self):
        @tracelogger(printer=lambda locals_: multiline_printer(locals_=locals_, width=30), width=30)
        def test_function(x):
            y = x**2
            return y

        y = test_function(x=2)
        self.assertEqual(y, 4)

    def test_non_keyword_arguments(self):
        @tracelogger(lambda locals_: multiline_printer(locals_=locals_, width=30), width=30)
        def test_function(x):
            y = x**2
            return y

        y = test_function(x=2)
        self.assertEqual(y, 4)

    def test_unknown_parameter_throws_error(self):
        with self.assertRaises(ValueError):

            @tracelogger(asd='asd')  # This needs to be defined here as the exception is thrown at declaration
            def test_function(x):
                y = x**2
                return y

            y = test_function(x=2)
            self.assertEqual(y, 4)
