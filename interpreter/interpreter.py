
from langGrammar import *
from interpreter.environment import Environment

from standardLib.std import *

class Interpreter:
    def __init__(self, AST: list[Grammar]) -> None:
        assert AST is not None
        self.AST: list[Grammar] = AST
        
        self.globalEnv = Environment()
        
        self.environment = Environment(self.globalEnv)

        self.bindSTD()

    def bindSTD(self):
        for key, value in standardFunctions.items():
            value.environment = self.environment
            self.globalEnv.define(key, value)

    def run(self):
        for statement in self.AST:
            statement.eval(self.environment)

