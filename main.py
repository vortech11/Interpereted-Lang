import sys
from pathlib import Path as Path

from scanner import Scanner
from parser import Parser
from langGramar import printAST

def parse_file(filePath):
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
        statement.eval()
    
    for statement in statementTree:
        printAST(statement)

if __name__ == "__main__":
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
