
from .terminaloh import clear_terminal


def log_return(func):
    def wrapper(*args, **kwargs):
        get = func(*args, **kwargs)
        print(get)
    return wrapper

# def iterator(func):
#     def wrapper(*args, **kwargs):
#         get = list(iter(map(func,*args)))
#         # get = func(*args, **kwargs)
#         print(get)
#     return wrapper


def boxed(func):
    def wrapper(*args, **kwargs):
        s = ""
        for item in args:
            s += f'{item} '
        s = s.strip()
        # print()
        st = f'|   {s}   |'
        box_len = len(st)
        print("-" * box_len)
        print(f'{st}')
        print("-" * box_len)
        # print()
    return wrapper


def bordered(func):
    def wrapper(*args, **kwargs):
        print("#" + "-" * 59)
        func(*args, **kwargs)
        print("#" + "-" * 59)
    return wrapper


def terminal_rolling(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        """
        The wrapper function is used to print a header and footer around the function it wraps.
        It also prints out the width of the terminal window, so that we can use it as a fixed-width for our text.

        :param *args: Pass a non-keyworded, variable-length argument list
        :param **kwargs: Collect all keyword arguments that are not
        :return: The value of the function that it wraps
        :doc-author: Trelent
        """
        headline = kwargs.get('headline')
        width = kwargs.get('width')
        # rows = kwargs.get('rows')

        clear_terminal()

        print(f'{headline:^{width}}')
        print("-" * (width))
        func(*args, **kwargs)
        print("-" * (width))
    return wrapper


def separator(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        separator = kwargs.get('separator')
        length = kwargs.get('length')
        if separator is None:
            separator = "*"
        if length is None:
            length = 60
        print(f'{separator} ' * int(round((length/(len(separator)+1)+1),1)))
        a = func(*args, **kwargs)
        s = a.splitlines()
        for i in s:
            ss = f'{i:{length}}{separator}'
            print(ss)
        print(f'{separator} ' * int(round((length/(len(separator)+1)+1),1)))
    return wrapper


def headline(func):
    def wrapper(*args, **kwargs):
        centering = 0
        c = kwargs.get('centering')
        if c is not None:
            centering = int(c)
        s = ""
        for item in args:
            s += f'{item} '
        s = s.strip()
        s = f'  {s}  '
        left = int((centering-len(s))/2)
        right = centering - int(left+len(s))
        st = "#" * left + s + "#" * right
        func(f'{st:^{centering}}')
        return func
    return wrapper


def topic(func):
    def wrapper(*args, **kwargs):
        centering = 0
        c = kwargs.get('centering')
        if c is not None:
            centering = int(c)
        s = ""
        for item in args:
            s += f'{item} '
        s = s.strip()
        st = f'# --- {s} --- #'
        func(f'{st:^{centering}}')
    return wrapper


def measure_time(func):
    def wrapper(*args, **kwargs):
        from time import time
        start = time()
        result = func(*args, **kwargs)
        print(f'Elapsed time is {time() - start} ms')
        return result
    return wrapper


def logger(func):
    from datetime import datetime
    def wrapper(*args, **kwargs):
        print('*' * 60)
        print(f'Run on: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
        print(func.__name__)
        func(*args, **kwargs)
        print('*' * 60)
    return wrapper



def threaded_deco(func):
    import threading
    """
    A decorator for any function that needs to be run on a separate thread
    """
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


def multiprocess_deco(func):
    import multiprocessing
    """
    A decorator for any function that needs to be run on a separate process
    """
    def wrapper(*args, **kwargs):
        process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        process.start()
        return process
    return wrapper
