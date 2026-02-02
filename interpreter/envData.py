from typing import Any


class Callable:
    def __init__(self, arity, environment, params=None, body=None) -> None:
        self.arity = arity
        self.environment = environment
        self.params = params
        self.body = body
    
    def call(self, arguments) -> Any:
        assert not (self.params is None or self.body is None)
        for index, param in enumerate(self.params):
            self.environment.define(param.lexeme, arguments[index])
        
        try:
            self.body.eval(self.environment)
        except ReturnValue as value:
            return value.value
    
class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value