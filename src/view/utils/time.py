
import functools
from threading import Timer
# debounce decorator function source:
# https://stackoverflow.com/questions/61476962/python-decorator-for-debouncing-including-function-arguments
# answer by Marquinho Peli
def debounce(timeout: float):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.func.cancel()
            wrapper.func = Timer(timeout, func, args, kwargs)
            wrapper.func.start()
        
        wrapper.func = Timer(timeout, lambda: None)
        return wrapper
    return decorator