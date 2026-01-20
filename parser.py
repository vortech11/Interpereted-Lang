from langGrammar import *
import logging
logger = logging.getLogger(__name__)

class Parser:
    def __init__(self, tokens: list[Token]):
        self.current: int = 0
        self.tokens: list[Token] = tokens
        
    def getToken(self, offset=0) -> Token:
        return self.tokens[self.current + offset]
        
    def getNextToken(self, offset = 0) -> Token:
        return self.tokens[self.current + 1 + offset]
    
    def isAtEnd(self, offset=0) -> bool:
        return self.getToken(offset).type == TokenType.EOF
        
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
        return self.assignment()
    
    def assignment(self) -> Expr:
        expr: Expr = self.logical_or()
        
        if self.getNextToken().type in [TokenType.EQUAL]:
            self.advance()
            equals: Token = self.getToken()
            self.advance()
            value = self.assignment()
            
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            
            self.error(equals, "Invalid assignment target.")
            
        return expr
    
    def logical_or(self) -> Expr:
        expr: Expr = self.logical_and()
        
        if self.getNextToken().type in [TokenType.OR]:
            self.advance()
            operator: Token = self.getToken()
            self.advance()
            right: Expr = self.logical_and()
            expr = Binary(expr, operator, right)
            
        return expr
    
    def logical_and(self) -> Expr:
        expr: Expr = self.equality()
        
        if self.getNextToken().type in [TokenType.AND]:
            self.advance()
            operator: Token = self.getToken()
            self.advance()
            right: Expr = self.equality()
            expr = Binary(expr, operator, right)
            
        return expr
    
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
    
    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after if.")
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
        
        thenBranch: Stmt = self.statement()
        elseBranch: Stmt | None = None
        if self.getToken().type == TokenType.ELSE:
            self.advance()
            elseBranch = self.statement()
        
        return IfStmt(condition, thenBranch, elseBranch)
        
    def block(self):
        statements: list[Stmt] = []

        while not self.isAtEnd() and not (self.getToken().type in [TokenType.RIGHT_BRACE]):
            self.advance()
            statements.append(self.declaration())
        
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        block = Block(statements)
        return block
    
    def statement(self):
        tokenType = self.getToken().type
        match tokenType:
            case TokenType.PRINT:
                self.advance()
                return self.printStatement()
            case TokenType.IF:
                self.advance()
                return self.ifStatement()
            case TokenType.RIGHT_BRACE:
                self.advance()
                return self.block()
            
            case _:
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

        