from scanner import Token, TokenType
from environment import Environment

class Grammar:
    def getPrint(self) -> str:
        return f"()"
    
    def eval(self, environment: Environment):
        return

class Expr(Grammar):
    ...

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
    
class Variable(Expr):
    def __init__(self, name: Token) -> None:
        self.name = name
        
    def getPrint(self):
        return f"{self.name}"
    
    def eval(self, environment: Environment):
        return environment.get(self.name.lexeme)

class Stmt(Grammar):
    ...
    
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
    
class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr | None) -> None:
        self.name: Token = name
        self.initializer: Expr | None = initializer
        
    def getPrint(self) -> str:
        if self.initializer == None:
            value = None
        else:
            value = self.initializer.getPrint()
        return f"{self.name} {value}"
    
    def eval(self, environment: Environment):
        if self.initializer is None:
            value = None
        else:
            value = self.initializer.eval(environment)
        environment.define(self.name.lexeme, value)

def printAST(grammar: Grammar):
    print(f"{grammar.getPrint()}")