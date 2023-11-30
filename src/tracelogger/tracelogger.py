import sys
from traceback import linecache


def default_printer(locals_):
    return ', '.join([f'{k}={v}' for k, v in locals_.items()])


def names_printer(locals_, names):
    return ', '.join([f'{k}={v}' for k, v in locals_.items() if k in names])


def multiline_printer(locals_, width=80):
    s = ' ' * width
    return '\n' + '\n'.join([f'{s}{k}={v}' for k, v in locals_.items()]) + '\n'


class trace_context:
    def __init__(self, name, printer=None, width=None):
        self.name = name
        self.printer = printer or default_printer
        self.width = width or 80
        self.old_trace = None

    def __enter__(self):
        print(f'\nEntering function: {self.name}')
        self.old_trace = sys.gettrace()
        sys.settrace(self.trace_calls)

    def __exit__(self, *args, **kwargs):
        sys.settrace(self.old_trace)

    def trace_calls(self, frame, event, arg):
        if event != 'call' or frame.f_code.co_name != self.name:
            return None
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        if event not in ['line', 'return']:
            return
        line = linecache.getline(frame.f_code.co_filename, frame.f_lineno, frame.f_globals).rstrip()
        print(f'{line.ljust(self.width)}locals: {self.printer(frame.f_locals)}')
        if event == 'return':
            prev_name = f'{self.old_trace.__self__.name}()' if self.old_trace else 'None'
            print(f'Returning from: {self.name}() to: {prev_name}\n')


def tracelogger(*args, **kwargs):
    if len(set(kwargs.keys()) - {'printer', 'width'}) > 0:
        raise ValueError('Unknown parameter(s)')
    if len(kwargs) == 0:
        func = args[0]

        def decorated_func(*func_args, **func_kwargs):
            with trace_context(func.__name__):
                return_value = func(*func_args, **func_kwargs)
            return return_value

        return decorated_func
    else:

        def wrapper(func):
            def decorated_func(*func_args, **func_kwargs):
                printer = kwargs.get('printer', args[0] if args else None)
                width = kwargs.get('width', args[1] if args and len(args) > 1 else None)
                with trace_context(func.__name__, printer=printer, width=width):
                    return_value = func(*func_args, **func_kwargs)
                return return_value

            return decorated_func

        return wrapper
