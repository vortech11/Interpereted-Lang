import sys
from pathlib import Path as Path

functions = ["print"]

def breakupListByChar(word, lookchar):
    output = [""]
    for char in word:
        if char == lookchar:
            output.append(lookchar)
            output.append("")
        else:
            output[-1] += char
    
    if output[-1] == "":
        output = output[:-1]
    
    return output

def breakupListByCharWrapper(list, char):
    splitTokens = []
    for token in list:
        splitTokens.extend(breakupListByChar(token, char))
    return splitTokens
    

def parse_line(line:str):
    tokens = line.split(" ")
    tokens = [x for x in tokens if not x == '']
    
    tokens = breakupListByCharWrapper(tokens, "(")
    tokens = breakupListByCharWrapper(tokens, ")")
    
    syntaxTree = []
    
    for index, token in enumerate(tokens):
        if token in functions and tokens[index + 1] == "(":
            syntaxTree.append({
                "dataType": "func",
                "params": tokens[index + 2:tokens.index(")", index + 1)]
            })
    
    return syntaxTree

def parse_file(filePath):
    filePath = Path(filePath)
    with open(filePath, "r") as file:
        fileData = ""
        for line in file:
            fileData += line
            
    lineData = "".join([x for x in fileData if not x == "\n"])
    
    lineData = parse_line(lineData)
            
    print(lineData)

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
                print(parse_line(user_input))


