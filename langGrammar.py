from scanner import Token, TokenType
from environment import Environment, CallableFactory

from envData import *

class Grammar:
    def getPrint(self) -> str:
        return f"()"
    
    def eval(self, environment: Environment):
        return

class Expr(Grammar):
    ...

class Assign(Expr):
    def __init__(self, name: Token, value: Expr) -> None:
        self.name: Token = name
        self.value: Expr = value
        
    def eval(self, environment: Environment):
        environment.setValue(self.name.lexeme, self.value.eval(environment))
    
    def getPrint(self) -> str:
        return f"{self.name.lexeme} = {self.value.getPrint()}"

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right
        
    def eval(self, environment: Environment):
        left = self.left.eval(environment)
        right = self.right.eval(environment)
        if left == None or right == None:
            return None
        match self.operator.type:
            case TokenType.EQUAL_EQUAL: return left == right
            case TokenType.BANG_EQUAL: return not left == right
            case TokenType.GREATER: return left > right
            case TokenType.GREATER_EQUAL: return left >= right
            case TokenType.LESS: return left < right
            case TokenType.LESS_EQUAL: return left <= right
            
            case TokenType.PLUS: return left + right
            case TokenType.MINUS: return left - right
            case TokenType.STAR: return left * right
            case TokenType.SLASH: return left / right
            
            case TokenType.AND: return left and right
            case TokenType.OR: return left or right
            
            case _: return None
        
    def getPrint(self) -> str:
        return f"{self.operator} ({self.left.getPrint()}) ({self.right.getPrint()})"
        
class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression
        
    def eval(self, environment: Environment):
        return self.expression.eval(environment)
    
    def getPrint(self) -> str:
        return f"group {self.expression.getPrint()}"
        
class Literal(Expr):
    def __init__(self, value):
        self.value = value
        
    def eval(self, environment: Environment):
        return self.value
        
    def getPrint(self) -> str:
        match self.value:
            case str():
                return f'"{self.value}"'
            case _:
                return f"{self.value}"
        
class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator: Token = operator
        self.right: Expr = right
        
    def eval(self, environment: Environment): # type: ignore
        value = self.right.eval(environment)
        match self.operator.type:
            case TokenType.BANG: return not value
            case TokenType.MINUS: 
                try:
                    return -float(value) # type: ignore
                except ValueError:
                    return None
            
            case _: return None
    
    def getPrint(self) -> str:
        return f"{self.operator} ({self.right.getPrint()})"
    
class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]) -> None:
        self.callee: Expr = callee
        self.paren: Token = paren
        self.arguments: list[Expr] = arguments
    
    def getPrint(self):
        listPrintArgs = [arg.getPrint() for arg in self.arguments]
        printArgs = ", ".join(listPrintArgs)
        return f"{self.callee.getPrint()} {self.paren} ({printArgs})"
    
    def eval(self, environment: Environment):
        arguments = [arg.eval(environment) for arg in self.arguments]

        return environment.callFunc(self.callee, arguments)

class Variable(Expr):
    def __init__(self, name: Token) -> None:
        self.name = name
        
    def getPrint(self):
        return f"{self.name}"
    
    def eval(self, environment: Environment):
        return environment.get(self.name.lexeme)

class Stmt(Grammar):
    ...

class Block(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements: list[Stmt] = statements
    
    def getPrint(self) -> str:
        output = []
        for statement in self.statements:
            output.append(statement.getPrint())
        return f"{'\n'.join(output)}"
    
    def eval(self, environment: Environment):
        subEnv: Environment = Environment(environment)
        for statement in self.statements:
            try:
                statement.eval(subEnv)
            except ReturnValue as value:
                raise value
    
class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression
        
    def getPrint(self) -> str:
        return f"{self.expression.getPrint()}"
    
    def eval(self, environment: Environment):
        self.expression.eval(environment)
        
class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def getPrint(self) -> str:
        return f"print ({self.expression.getPrint()})"
    
    def eval(self, environment: Environment):
        print(self.expression.eval(environment))

class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr | None):
        self.keyword: Token = keyword
        self.value: Expr | None = value
    
    def getPrint(self) -> str:
        value = ""
        if not self.value is None:
            value = self.value.getPrint()
        return f"{self.keyword.lexeme} {value}"
    
    def eval(self, environment: Environment):
        value = None
        if not self.value is None:
            value = self.value.eval(environment)
        
        raise ReturnValue(value)
    
class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr | None) -> None:
        self.name: Token = name
        self.initializer: Expr | None = initializer
        
    def getPrint(self) -> str:
        if self.initializer == None:
            value = None
        else:
            value = self.initializer.getPrint()
        return f"var {self.name} {value}"
    
    def eval(self, environment: Environment):
        if self.initializer is None:
            value = None
        else:
            value = self.initializer.eval(environment)
        environment.define(self.name.lexeme, value)

class Function(Stmt):
    def __init__(self, name: Token, params: list[Token], body: Stmt) -> None:
        self.name: Token = name
        self.params: list[Token] = params
        self.body: Stmt = body
    
    def getPrint(self) -> str:
        params = ", ".join([str(param) for param in self.params])
        return f"func {self.name} ({params}) {{{self.body}}}"
    
    def eval(self, environment: Environment):
        funcFactory = CallableFactory(environment, self.params, self.body)

        environment.define(self.name.lexeme, funcFactory)

class IfStmt(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt | None) -> None:
        self.condition: Expr = condition
        self.thenBranch: Stmt = thenBranch
        self.elseBranch: Stmt | None = elseBranch

    def getPrint(self) -> str:
        return f"if ({self.condition.getPrint()}) {{{self.thenBranch.getPrint()}}}"
    
    def eval(self, environment: Environment):
        if self.condition.eval(environment) == True:
            self.thenBranch.eval(environment)
        elif not self.elseBranch is None:
            self.elseBranch.eval(environment)

class WhileStmt(Stmt):
    def __init__(self, expression: Expr, statement: Stmt) -> None:
        self.expression = expression
        self.statement = statement

    def getPrint(self) -> str:
        return f"while ({self.expression.getPrint()}) {{{self.statement.getPrint()}}}"
    
    def eval(self, environment: Environment):
        while self.expression.eval(environment):
            self.statement.eval(environment)
        
def printAST(grammar: Grammar):
    print(f"{grammar.getPrint()}")