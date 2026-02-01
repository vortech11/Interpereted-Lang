from time import ctime

from envData import *

class clock(Callable):
    def __init__(self) -> None:
        super().__init__(0, None)
    
    def call(self, arguments):
        return ctime()

standardFunctions = {
    "clock" : clock()
}

