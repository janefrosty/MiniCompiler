from lexer.lexer import Lexer, TokenType
from mast.node import Program, FunctionDecl, VarDecl, ReturnStmt, BinaryExpr, LiteralExpr, IdentifierExpr
from typing import List

class Parser:
    def __init__(self, source: str):
        self.lexer = Lexer(source)
        self.tokens = self.lexer.scan_tokens()
        self.current = 0

    def parse(self) -> Program:
        functions = []
        while not self._is_at_end():
            functions.append(self._function_decl())
        return Program(functions)

    def _function_decl(self):
        self._consume(TokenType.KW_FN)
        name = self._consume(TokenType.IDENTIFIER).lexeme
        self._consume(TokenType.LPAREN)
        params = []
        if not self._check(TokenType.RPAREN):
            params = self._param_list()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.LBRACE)
        body = self._block()          # <-- вот этот метод был пропущен
        self._consume(TokenType.RBRACE)
        return FunctionDecl(name, params, body)

    def _param_list(self):
        params = [self._param()]
        while self._match(TokenType.COMMA):
            params.append(self._param())
        return params

    def _param(self):
        self._consume(TokenType.KW_INT)
        return self._consume(TokenType.IDENTIFIER).lexeme

    def _block(self):
        statements = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            statements.append(self._statement())
        return statements

    def _statement(self):
        if self._match(TokenType.KW_INT):
            name = self._consume(TokenType.IDENTIFIER).lexeme
            self._consume(TokenType.ASSIGN)
            value = self._expression()
            self._consume(TokenType.SEMICOLON)
            return VarDecl(name, value)
        if self._match(TokenType.KW_RETURN):
            value = self._expression()
            self._consume(TokenType.SEMICOLON)
            return ReturnStmt(value)
        return self._expression_stmt()

    def _expression_stmt(self):
        expr = self._expression()
        self._consume(TokenType.SEMICOLON)
        return expr

    def _expression(self):
        return self._equality()

    def _equality(self):
        expr = self._comparison()
        while self._match(TokenType.EQ, TokenType.NEQ):
            op = self._previous().lexeme
            right = self._comparison()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op = self._previous().lexeme
            right = self._term()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _term(self):
        expr = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous().lexeme
            right = self._factor()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _factor(self):
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            op = self._previous().lexeme
            right = self._unary()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _unary(self):
        if self._match(TokenType.NOT, TokenType.MINUS):
            op = self._previous().lexeme
            right = self._unary()
            return BinaryExpr(None, op, right)
        return self._primary()

    def _primary(self):
        if self._match(TokenType.INT_LITERAL):
            return LiteralExpr(self._previous().literal)
        if self._match(TokenType.IDENTIFIER):
            return IdentifierExpr(self._previous().lexeme)
        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN)
            return expr
        raise Exception(f'Unexpected token: {self._peek().type.name}')

    # Вспомогательные методы
    def _consume(self, typ):
        if self._check(typ):
            return self._advance()
        raise Exception(f'Expected {typ.name}, got {self._peek().type.name}')

    def _match(self, *types):
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _check(self, typ):
        if self._is_at_end(): return False
        return self._peek().type == typ

    def _advance(self):
        self.current += 1
        return self.tokens[self.current - 1]

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _is_at_end(self):
        return self._peek().type == TokenType.EOF
