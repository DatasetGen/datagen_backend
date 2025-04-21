from typing import Generic, TypeVar, Callable, Union

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")

class Result(Generic[T, E]):
    def __init__(self, is_ok: bool, value: Union[T, E]):
        self._is_ok = is_ok
        self._value = value

    @staticmethod
    def ok(value: T) -> 'Result[T, E]':
        return Result(True, value)

    @staticmethod
    def failure(error: E) -> 'Result[T, E]':
        return Result(False, error)

    @staticmethod
    def wrap(fn: Callable[[], T]) -> 'Result[T, Exception]':
        try:
            return Result.ok(fn())
        except Exception as e:
            return Result.failure(e)

    @property
    def is_ok(self) -> bool:
        return self._is_ok

    @property
    def is_failure(self) -> bool:
        return not self._is_ok

    def unwrap(self) -> T:
        if self._is_ok:
            return self._value  # type: ignore
        raise ValueError(f"Called unwrap on failure: {self._value}")

    def unwrap_or(self, default: T) -> T:
        return self._value if self._is_ok else default  # type: ignore

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        return self._value if self._is_ok else fn(self._value)  # type: ignore

    def map(self, fn: Callable[[T], U]) -> 'Result[U, E]':
        if self._is_ok:
            try:
                return Result.ok(fn(self._value))  # type: ignore
            except Exception as e:
                return Result.failure(e)  # type: ignore
        return Result.failure(self._value)  # type: ignore

    def bind(self, fn: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        if self._is_ok:
            try:
                return fn(self._value)
            except Exception as e:
                return Result.failure(e)
        return Result.failure(self._value)
