import os
import os.path
from functools import wraps
from pathlib import Path
from typing import Any, Callable

main_path = Path(__file__).resolve().parents[1]
path = os.path.join(main_path, "logs", "logging.txt")
flags = os.O_RDWR | os.O_CREAT
if os.path.exists(path):
    os.remove(path)
log_file = os.open(path, flags)


def log(filename: str | None = None) -> Callable:
    """Декоратор логирующий работу и результат функции в консоль или файл"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                os.write(log_file, "\nНачало работы\n\n".encode())
                result = func(*args, **kwargs)
                log_massage = "my_function ok"
                os.write(log_file, f"{log_massage}\n\nКонец работы".encode())
                if not filename:
                    print(log_massage)
                return result
            except Exception as e:
                log_message = f"my_function error: {e}, Inputs: ({args}, {kwargs})"
                os.write(log_file, log_message.encode() + "\n\nКонец работы".encode())
                if not filename:
                    print(log_message)

        return wrapper

    return decorator


@log(filename="")
def my_function(x: int, y: int) -> Any:
    """Суммирование"""
    return x + y


my_function(3, 0)
