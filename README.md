I wrote this before I learnt about *Snoop*: [https://github.com/alexmojaki/snoop](https://github.com/alexmojaki/snoop) a much polished version of the same concept and implementation with an additional set of debug tools.

# Tracelogger

Tag your functions with the `@tracelogger` decorator to be logged line-by-line.

Optionally provide a function as the `printer` argument that takes the local variable dictionary and returns a string. This allows the customisation of which variables and how you want to print at each line. See the example with the provided `names_printer` function that only prints a selected set of variables.

The second `width` parameter determines the maximum character number for each line of code defaulting to `80`.

```
from tracelogger import tracelogger, names_printer


@tracelogger(width=30)
def second_test_function(x):
    y = x**2
    return y


@tracelogger(printer=lambda locals_: names_printer(locals_=locals_, names=['k', 'b']), width=30)
def first_test_function(a, b):
    c = a + b
    for k in range(5):
        if k % 2 == 0:
            b += k
        else:
            c += k
            second_test_function(c)
    return a, b, c

a, b, c = first_test_function(a=10, b=20)
```

This will print the following:

```
Entering function: first_test_function
    c = a + b                            locals: b=20
    for k in range(5):                   locals: b=20
        if k % 2 == 0:                   locals: b=20, k=0
            b += k                       locals: b=20, k=0
    for k in range(5):                   locals: b=20, k=0
        if k % 2 == 0:                   locals: b=20, k=1
            c += k                       locals: b=20, k=1
            second_test_function(c)      locals: b=20, k=1

Entering function: second_test_function
    y = x**2                             locals: x=31
    return y                             locals: x=31, y=961
    return y                             locals: x=31, y=961
Returning from: second_test_function() to: first_test_function()

    for k in range(5):                   locals: b=20, k=1
        if k % 2 == 0:                   locals: b=20, k=2
            b += k                       locals: b=20, k=2
    for k in range(5):                   locals: b=22, k=2
        if k % 2 == 0:                   locals: b=22, k=3
            c += k                       locals: b=22, k=3
            second_test_function(c)      locals: b=22, k=3

Entering function: second_test_function
    y = x**2                             locals: x=34
    return y                             locals: x=34, y=1156
    return y                             locals: x=34, y=1156
Returning from: second_test_function() to: first_test_function()

    for k in range(5):                   locals: b=22, k=3
        if k % 2 == 0:                   locals: b=22, k=4
            b += k                       locals: b=22, k=4
    for k in range(5):                   locals: b=26, k=4
    return a, b, c                       locals: b=26, k=4
    return a, b, c                       locals: b=26, k=4
Returning from: first_test_function() to: None
```

Join the [Code Quality for Data Science (CQ4DS) Discord channel](https://discord.com/invite/8uUZNMCad2) for feedback.

I used the following StackOverflow threads as sources, many thanks to their authors:

[https://stackoverflow.com/questions/32163436/python-decorator-for-printing-every-line-executed-by-a-function](https://stackoverflow.com/questions/32163436/python-decorator-for-printing-every-line-executed-by-a-function)

[https://stackoverflow.com/questions/22362940/inspect-code-of-next-line-in-python](https://stackoverflow.com/questions/22362940/inspect-code-of-next-line-in-python)
