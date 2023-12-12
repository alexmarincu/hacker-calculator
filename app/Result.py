class Result:
    pass


class Success(Result):
    def __init__(self, value):
        self.value = value


class Failure(Result):
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage
