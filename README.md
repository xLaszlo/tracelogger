# tracelogger

Tag your functions to be logged line-by-line with the `@tracelogger`, optionally add a list of names to print each time

```
@tracelogger
def second_test_function(x):
    y = x**2
    return y


@tracelogger(names=['b', 'k'])
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

Will result in:

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
