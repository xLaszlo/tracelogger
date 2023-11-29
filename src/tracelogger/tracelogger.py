import sys
from traceback import linecache


class trace_context:
    def __init__(self, name, names=None):
        self.name = name
        self.names = names
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
        locals_ = {k: v for k, v in frame.f_locals.items() if self.names is None or k in self.names}
        locals_ = ', '.join([f'{k}={v}' for k, v in locals_.items()])
        print(f'{line.ljust(40)} locals: {locals_}')
        if event == 'return':
            prev_name = f'{self.old_trace.__self__.name}()' if self.old_trace else 'None'
            print(f'Returning from: {self.name}() to: {prev_name}\n')


def tracelogger(*args, **kwargs):
    if len(args) == 1 and callable(args[0]) and not kwargs:
        func = args[0]

        def decorated_func(*func_args, **func_kwargs):
            with trace_context(func.__name__):
                return_value = func(*func_args, **func_kwargs)
            return return_value

        return decorated_func
    else:

        def wrapper(func):
            def decorated_func(*func_args, **func_kwargs):
                names = kwargs.get('names', args[0] if args else None)
                with trace_context(func.__name__, names=names):
                    return_value = func(*func_args, **func_kwargs)
                return return_value

            return decorated_func

        return wrapper
