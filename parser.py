from langGramar import *
import logging
logger = logging.getLogger(__name__)

class Parser:
    def __init__(self, tokens: list[Token]):
        self.current: int = 0
        self.tokens: list[Token] = tokens
        
    def getToken(self) -> Token:
        return self.tokens[self.current]
        
    def getNextToken(self, offset = 0) -> Token:
        return self.tokens[self.current + 1 + offset]
    
    def isAtEnd(self) -> bool:
        return self.getToken().type == TokenType.EOF
        
    def advance(self):
        self.current += 1
        
    def error(self, token: Token, message: str):
        lexeme = None
        if token.type == TokenType.EOF:
            lexeme = "at end"
        else:
            lexeme = f"at '{token.lexeme}'"
        logger.error(f"{token.line} {lexeme} {message}")
    
    def consume(self, type: TokenType, message):
        if self.getNextToken().type == type:
            self.advance()
            return self.getToken()
        
        self.error(self.getNextToken(), message)
        return Token(TokenType.NIL, "", None, 0)
    
    def expression(self):
        return self.equality()
    
    def equality(self) -> Expr:
        expr: Expr = self.comparison()
        
        while self.getNextToken().type in [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]:
            self.advance()
            operator: Token = self.getToken()
            self.advance()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
            
        return expr
    
    def comparison(self) -> Expr:
        expr: Expr = self.term()
        
        while self.getNextToken().type in [TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]:
            self.advance()
            operator: Token = self.getToken()
            self.advance()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
            
        return expr
    
    def term(self) -> Expr:
        expr: Expr = self.factor()
        
        while self.getNextToken().type in [TokenType.MINUS, TokenType.PLUS]:
            self.advance()
            operator: Token = self.getToken()
            self.advance()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)
            
        return expr
    
    def factor(self) -> Expr:
        expr: Expr = self.unary()
        
        while self.getNextToken().type in [TokenType.SLASH, TokenType.STAR]:
            self.advance()
            operator: Token = self.getToken()
            self.advance()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)
            
        return expr
    
    def unary(self) -> Expr:
        if self.getToken().type in [TokenType.BANG, TokenType.MINUS]:
            operator: Token = self.getToken()
            self.advance()
            right: Expr = self.unary()
            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self) -> Expr:
        match self.getToken().type:
            case TokenType.FALSE: return Literal(False)
            case TokenType.TRUE: return Literal(True)
            case TokenType.NIL: return Literal(None)
            case TokenType.NUMBER | TokenType.STRING: return Literal(self.getToken().literal)
            case TokenType.LEFT_PAREN: 
                self.advance()
                expr: Expr = self.expression()
                self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
                return Grouping(expr)
            
            case TokenType.IDENTIFIER: return Variable(self.getToken())
            
            case _: 
                self.error(self.getToken(), "Expect expression")
                return Expr()
    
    def printStatement(self):
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)
    
    def expressionStatement(self):
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(expr)
    
    def statement(self):
        if self.getToken().type == TokenType.PRINT:
            self.advance()
            return self.printStatement()

        return self.expressionStatement()
    
    def varDeclaration(self):
        name: Token = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        
        initializer: Expr | None = None
        if self.getNextToken().type in [TokenType.EQUAL]:
            self.advance()
            self.advance()
            initializer = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)
    
    def declaration(self):
        if self.getToken().type in [TokenType.VAR]:
            return self.varDeclaration()
        
        else:
            return self.statement()
    
    def parse(self):
        tokenList = []
        while not self.isAtEnd():
            tokenList.append(self.declaration())
            self.advance()
        return tokenList

        