from scanner import Token, TokenType

class Grammar:
    def getPrint(self) -> str:
        return f"()"
    
    def eval(self):
        return

class Expr(Grammar):
    ...

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right
        
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
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
        
    def eval(self):
        return self.expression.eval()
    
    def getPrint(self) -> str:
        return f"group {self.expression.getPrint()}"
        
class Literal(Expr):
    def __init__(self, value):
        self.value = value
        
    def eval(self):
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
        
    def eval(self): # type: ignore
        value = self.right.eval()
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
    
    def eval(self): # type: ignore
        return (self.name.lexeme)

class Stmt(Grammar):
    def __init__(self, previous: Grammar | None, next: Grammar | None) -> None:
        self.next: Grammar | None = next
        self.previous: Grammar | None = previous
    
class Expression(Stmt):
    def __init__(self, expression: Expr, previous: Grammar | None, next: Grammar | None = None):
        super().__init__(previous, next)
        self.expression: Expr = expression
        
    def getPrint(self) -> str:
        output = f"{self.expression.getPrint()}\n"
        if self.next is not None:
            output += f"{self.next.getPrint()}"
        return output
    
    def eval(self):
        self.expression.eval()
        if self.next is not None:
            self.next.eval()
        
class Print(Stmt):
    def __init__(self, expression: Expr, previous: Grammar | None, next: Grammar | None = None):
        super().__init__(previous, next)
        self.expression: Expr = expression

    def getPrint(self) -> str:
        output = f"print ({self.expression.getPrint()})"
        if self.next is not None:
            output += f"\n{self.next.getPrint()}"
        return output
    
    def eval(self):
        print(self.expression.eval())
        if self.next is not None:
            self.next.eval()
    
class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr, previous: Grammar | None, next: Grammar | None = None) -> None:
        super().__init__(previous, next)
        self.name = name
        self.initializer = initializer
        
    def getPrint(self) -> str:
        output = f"{self.name} {self.initializer.getPrint()}"
        if self.next is not None:
            output += f"\n{self.next.getPrint()}"
        return output

def printAST(grammar: Grammar):
    print(f"{grammar.getPrint()}")