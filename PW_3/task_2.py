#2.1
import functools
import time

def cache(max_size: int = 128):
    def decorator(func):
        _cache = {}
        _call_order = []

        @functools.wraps(func)
        def wrapper(*args):
            if args in _cache:
                print(f" {func.__name__}{args}")
                return _cache[args]
            
            print(f" {func.__name__}{args}")
            result = func(*args)
            _cache[args] = result
            _call_order.append(args)
            
            if len(_cache) > max_size:
                oldest_args = _call_order.pop(0)
                del _cache[oldest_args]
                
            return result

        wrapper.cache_info = lambda: {"size": len(_cache), "max_size": max_size}
        wrapper.cache_clear = lambda: (_cache.clear(), _call_order.clear())
        return wrapper
    return decorator


def rate_limit(max_calls: int, period: float = 60.0):
    def decorator(func):
        call_times = []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            call_times[:] = [t for t in call_times if current_time - t <= period]
            
            if len(call_times) >= max_calls:
                raise RuntimeError(f"Перевищено ліміт викликів ({max_calls} за {period}с)")
                
            call_times.append(current_time)
            return func(*args, **kwargs)

        return wrapper
    return decorator


def log(level: str = "INFO"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Виклик {func.__name__}(args={args}, kwargs={kwargs})")
            start = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start
                print(f"[{level}] {func.__name__} → {result} (час: {elapsed:.4f}с)")
                return result
            except Exception as e:
                print(f" {func.__name__} викликав помилку {e}")
                raise
        return wrapper
    return decorator


@cache(max_size=64)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@rate_limit(max_calls=5, period=10.0)
def send_notification(message: str) -> str:
    return f"Надіслано: {message}"

@log(level="DEBUG")
def divide(a: float, b: float) -> float:
    return a / b


def main():
    print(" тестування @cache")
    fibonacci(30)
    print("Cache Info:", fibonacci.cache_info())
    
    print("\n mестування @rate_limit")
    for i in range(6):
        try:
            print(send_notification(f"Повідомлення {i+1}"))
        except RuntimeError as e:
            print(f"Помилка на кроці {i+1}: {e}")
            
    print("\n--- Тестування @log ---")
    divide(10, 2)
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass

if __name__ == "__main__":
    main()


#2.2

import functools

def auto_repr(cls):
    co_varnames = cls.__init__.__code__.co_varnames
    arg_count = cls.__init__.__code__.co_argcount
    init_args = co_varnames[1:arg_count]

    def __repr__(self):
        args_str = ", ".join(f"{arg}={getattr(self, arg, None)}" for arg in init_args)
        return f"{cls.__name__}({args_str})"

    cls.__repr__ = __repr__
    return cls


def frozen(cls):
    original_init = cls.__init__

    @functools.wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        # Встановлюємо прапорець напряму через базовий клас, щоб обійти __setattr__
        object.__setattr__(self, "_frozen", True)

    def new_setattr(self, name, value):
        if getattr(self, "_frozen", False):
            raise AttributeError(f"Неможливо змінити '{name}' - об'єкт заморожений")
        object.__setattr__(self, name, value)

    cls.__init__ = new_init
    cls.__setattr__ = new_setattr
    return cls


def log_methods(cls):
    for attr_name in dir(cls):
        if not attr_name.startswith("_"):
            attr_value = getattr(cls, attr_name)
            if callable(attr_value):
                @functools.wraps(attr_value)
                def wrapper(self, *args, **kwargs):
                    print(f"[LOG METHOD] Виклик {cls.__name__}.{attr_value.__name__}")
                    result = attr_value(self, *args, **kwargs)
                    print(f"[LOG METHOD] Результат {cls.__name__}.{attr_value.__name__}: {result}")
                    return result
                setattr(cls, attr_name, wrapper)
    return cls


@auto_repr
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@frozen
class ImmutableConfig:
    def __init__(self, host: str, port: int, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug


@log_methods
class MathService:
    def add(self, a: float, b: float) -> float:
        return a + b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Ділення на нуль")
        return a / b


def main():
    print("Тестування @auto_repr")
    p = Point(3.0, 4.0)
    print(repr(p))

    print("\nТестування @frozen")
    cfg = ImmutableConfig("localhost", 8080, debug=True)
    print(f"Config: {cfg.host}:{cfg.port}")
    try:
        cfg.host = "remote"  
    except AttributeError as e:
        print(f"Очікувана помилка: {e}")

    print("\nТестування @log_methods")
    svc = MathService()
    svc.add(10, 20)
    svc.multiply(3, 7)
    try:
        svc.divide(10, 0)
    except ValueError as e:
        print(f"Зловлено помилку {e}")

if __name__ == "__main__":
    main()

