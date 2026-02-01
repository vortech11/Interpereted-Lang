


class Callable:
    def __init__(self, arity) -> None:
        self.arity = arity
    
    def call(self, environment, arguments):
        ...