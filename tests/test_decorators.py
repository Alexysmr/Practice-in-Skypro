from typing import Any
from src.decorators import log


def test_log() -> Any:
    """Тестирование декорируемой функции my_function при отсутствии filename"""

    @log(filename="")
    def my_function(x: int, y: int) -> Any:
        """Сложение"""
        return x + y

    result = my_function(3, -1)
    assert result == 2


def test_log_no_filename(capsys: Any) -> Any:
    """Перехват вывода в консоль при решении и отсутствии filename"""

    @log(filename="")
    def func(x: int, y: int) -> Any:
        """Сложение"""
        return x + y

    func(3, -1)
    captured = capsys.readouterr()
    assert captured.out == "my_function ok\n"


def test_log_filename_exception(capsys: Any) -> Any:
    """Перехват вывода в консоль статуса решения при указанном filename"""

    @log(filename="logs/logging.txt")
    def func(x: int, y: int) -> Any:
        """Деление"""
        return x / y

    func(3, 1)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_log_filename_exception_no_solution(capsys: Any) -> Any:
    """Перехват вывода в консоль статуса при отсутствии решения и указанном filename"""

    @log(filename="logs/logging.txt")
    def func(x: int, y: int) -> Any:
        """Деление на ноль"""
        return x / y

    func(3, 0)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_log_no_filename_exception(capsys: Any) -> Any:
    """Перехват вывода в консоль при отсутствии решения и filename"""

    @log(filename="")
    def func(x: int, y: int) -> Any:
        """Деление"""
        return x / y

    func(3, 0)
    captured = capsys.readouterr()
    assert captured.out == "my_function error: division by zero, Inputs: ((3, 0), {})\n"
