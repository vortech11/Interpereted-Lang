
from langGrammar import *
from environment import Environment


class Interpreter:
    def __init__(self, AST: list[Grammar]) -> None:
        assert AST is not None
        self.AST: list[Grammar] = AST
        
        globalEnv = Environment()
        
        self.environment = Environment(globalEnv)
                
    def run(self):
        for statement in self.AST:
            statement.eval(self.environment)

