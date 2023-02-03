from functools import lru_cache, wraps
from datetime import datetime, timedelta


# JWT token plugin has 604800 seconds cache by default
def timed_lru_cache(seconds: int, maxsize: int = 604800):  # type: ignore
    def wrapper_cache(func):  # type: ignore
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):  # type: ignore
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
