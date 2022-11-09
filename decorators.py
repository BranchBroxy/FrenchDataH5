def get_time(func):
    from time import perf_counter
    from functools import wraps
    """Times any function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        total_time = round(end_time - start_time, 5)
        print(f"Took a total time of {total_time} seconds to run {func.__name__}\n")
        return result
    return wrapper