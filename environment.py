import logging
logger = logging.getLogger(__name__)

class Environment:
    def __init__(self) -> None:
        self.values: dict = {}
        
    def define(self, name, value):
        if name not in self.values:
            self.values[name] = value
        else:
            logger.error(f"Variable {name} already instantiated")
        
    def get(self, name):
        if name in self.values:
            return self.values[name]
        else:
            logger.error(f"Undefined variable {name}.")
            exit()

    def setValue(self, name, value):
        if name in self.values:
            self.values[name] = value
        else:
            logger.error(f"Undefined variable {name}.")
            exit()