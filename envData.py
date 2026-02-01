from typing import Any


class Callable:
    def __init__(self, arity, environment) -> None:
        self.arity = arity
        self.environment = environment
    
    def call(self, arguments) -> Any:
        ...