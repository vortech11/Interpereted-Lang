import logging
logger = logging.getLogger(__name__)

class Environment:
    def __init__(self) -> None:
        self.values: dict = {}
        
    def define(self, name, value) -> None:
        self.values[name] = value
        
    def get(self, name):
        if name in self.values:
            return self.values[name]
        else:
            logger.error(f"Undefined variable {name}.")
            exit()