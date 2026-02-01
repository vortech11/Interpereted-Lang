import logging
logger = logging.getLogger(__name__)

import envData

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

    def callFunc(self, name, parameters):
        ...