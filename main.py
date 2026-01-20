import sys
from pathlib import Path as Path
import logging

from scanner import Scanner
from parser import Parser
from interpreter import Interpreter
from langGrammar import printAST

logger = logging.getLogger(__name__)


def parse_file(filePath):
    loggingLevel = logging.WARNING
    logging.basicConfig(level=loggingLevel)
    logger.info('Started')
    
    filePath = Path(filePath)
    with open(filePath, "r") as file:
        fileData = ""
        for line in file:
            fileData += line
    #print(fileData)
    
    scanner = Scanner(fileData)
    tokens = scanner.scanTokens()
    
    parser = Parser(tokens)
    statementTree = parser.parse()
    
    for statement in statementTree:
        logger.debug(statement.getPrint())
    
    interpreter = Interpreter(statementTree)
    interpreter.run()
        
    logger.info('Finished')

def main():
    running = True
    while running:
        if len(sys.argv[1:]) > 0:
            parse_file(sys.argv[1])
            running = False
        else:
            user_input = input(">>> ")

            if user_input == "exit":
                running = False
            else:
                print(user_input)

if __name__ == "__main__":
    main()