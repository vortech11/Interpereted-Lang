import logging
logger = logging.getLogger(__name__)

from interpreter.envData import *

class CallableFactory:
    def __init__(self, parentEnv, params, body) -> None:
        self.arity = len(params)
        self.params = params
        self.body = body
        self.parentEnv = parentEnv
    
    def constructCallable(self) -> Callable:
        funcEnv = Environment(self.parentEnv)
        return Callable(self.arity, funcEnv, self.params, self.body)

class Environment:
    def __init__(self, parentEnv = None) -> None:
        self.parentEnv: Environment | None = None
        if not parentEnv is None:
            self.parentEnv = parentEnv
        self.values: dict = {}
        
    def checkParentNamespace(self, name) -> list:
        if name in self.values:
            return [self, self.values[name]]
        
        if not self.parentEnv is None:
            value = self.parentEnv.checkParentNamespace(name)
        else:
            value = [None, None]
        return value

    def define(self, name, value):
        if name not in self.values:
            self.values[name] = value
        else:
            logger.error(f"Variable {name} already instantiated")
        
    def get(self, name):
        value = self.checkParentNamespace(name)[1]
        if name in self.values:
            return self.values[name]
        elif not value is None:
            return value
        else:
            logger.error(f"Undefined variable {name}.")
            exit()

    def setValue(self, name, value):
        globalValue = self.checkParentNamespace(name)
        
        if name in self.values:
            self.values[name] = value
        elif not globalValue == [None, None]:
            globalValue[0].values[name] = value
        else:
            logger.error(f"Undefined variable {name}.")
            exit()

    def callFunc(self, expr, parameters):
        func = expr.eval(self)
        if not isinstance(func, CallableFactory):
            if not isinstance(func, Callable):
                logger.error(f"Function expression '{expr.getPrint()}' is not callable.")
                exit()
            
            if not len(parameters) == func.arity:
                logger.error(f"Function expression '{expr.getPrint()}' expected {func.arity} arguments but got {len(parameters)}.")
                exit()

            return func.call(parameters)
        
        if not len(parameters) == func.arity:
            logger.error(f"Function expression '{expr.getPrint()}' expected {func.arity} arguments but got {len(parameters)}.")
            exit()
        
        callableFunc = func.constructCallable()

        return callableFunc.call(parameters)

