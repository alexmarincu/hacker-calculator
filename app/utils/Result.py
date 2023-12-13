import typing as tp
T = tp.TypeVar('T')


class Result(tp.Generic[T]):
    pass


class Success(Result[T]):
    def __init__(self, value: T):
        self.value = value


class Failure(Result[T]):
    def __init__(self, errorMessage: str):
        self.errorMessage = errorMessage
