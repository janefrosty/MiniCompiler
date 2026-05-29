from lexer.lexer import Lexer, TokenType
from mast.node import (
    Program, FunctionDecl, VarDecl, ReturnStmt, IfStmt, WhileStmt,
    BinaryExpr, LiteralExpr, IdentifierExpr, CallExpr,
    ArrayDecl, ArraySubscript  
)
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
        params = self._param_list() if not self._check(TokenType.RPAREN) else []
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.LBRACE)
        body = self._block()
        self._consume(TokenType.RBRACE)
        return FunctionDecl(name, params, body)

    def _param_list(self):
        params = [self._param()]
        while self._match(TokenType.COMMA):
            params.append(self._param())
        return params

    def _param(self):
        if self._match(TokenType.KW_INT):
            return self._consume(TokenType.IDENTIFIER).lexeme
        return self._consume(TokenType.IDENTIFIER).lexeme

    def _block(self):
        statements = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            statements.append(self._statement())
        return statements

    def _statement(self):
        if self._match(TokenType.KW_INT):
            name = self._consume(TokenType.IDENTIFIER).lexeme
            if self._check(TokenType.LBRACKET):
                return self._array_decl(name)
            self._consume(TokenType.ASSIGN)
            value = self._expression()
            self._consume(TokenType.SEMICOLON)
            return VarDecl(name, value)

        if self._match(TokenType.KW_IF):
            return self._if_statement()
        if self._match(TokenType.KW_WHILE):
            return self._while_statement()
        if self._match(TokenType.KW_RETURN):
            value = self._expression()
            self._consume(TokenType.SEMICOLON)
            return ReturnStmt(value)

        if self._check(TokenType.IDENTIFIER):
            saved = self.current
            left = self._primary() 
            if self._match(TokenType.ASSIGN):
                right = self._expression()
                self._consume(TokenType.SEMICOLON)
                return BinaryExpr(left, '=', right)
            self.current = saved

        return self._expression_stmt()

    def _array_decl(self, name: str):
        dimensions = []
        while self._match(TokenType.LBRACKET):
            dim_expr = self._expression()
            dimensions.append(dim_expr)
            self._consume(TokenType.RBRACKET)
        self._consume(TokenType.SEMICOLON)
        return ArrayDecl(name, dimensions, None)

    def _if_statement(self):
        self._consume(TokenType.LPAREN)
        condition = self._expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.LBRACE)
        then_body = self._block()
        self._consume(TokenType.RBRACE)
        else_body = None
        if self._match(TokenType.KW_ELSE):
            self._consume(TokenType.LBRACE)
            else_body = self._block()
            self._consume(TokenType.RBRACE)
        return IfStmt(condition, then_body, else_body)

    def _while_statement(self):
        self._consume(TokenType.LPAREN)
        condition = self._expression()
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.LBRACE)
        body = self._block()
        self._consume(TokenType.RBRACE)
        return WhileStmt(condition, body)

    def _expression_stmt(self):
        expr = self._expression()
        self._consume(TokenType.SEMICOLON)
        return expr

    def _expression(self):
        return self._assignment()

    def _assignment(self):
        left = self._equality()
        if self._match(TokenType.ASSIGN):
            right = self._assignment()
            if not isinstance(left, (IdentifierExpr, ArraySubscript)):
                raise Exception("Left-hand side of assignment must be a variable or array element")
            return BinaryExpr(left, '=', right)
        return left

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
            name = self._previous().lexeme
            # Вызов функции
            if self._check(TokenType.LPAREN):
                return self._call_expr(name)
            # Доступ к элементу массива
            expr = IdentifierExpr(name)
            while self._match(TokenType.LBRACKET):
                index = self._expression()
                self._consume(TokenType.RBRACKET)
                expr = ArraySubscript(expr, [index])
            return expr

        if self._match(TokenType.KW_TRUE):
            return LiteralExpr(True)
        if self._match(TokenType.KW_FALSE):
            return LiteralExpr(False)

        # Скобочное выражение
        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN)
            return expr

        raise Exception(f'Unexpected token: {self._peek().type.name}')

    def _call_expr(self, name: str):
        self._consume(TokenType.LPAREN)
        args = []
        if not self._check(TokenType.RPAREN):
            args.append(self._expression())
            while self._match(TokenType.COMMA):
                args.append(self._expression())
        self._consume(TokenType.RPAREN)
        return CallExpr(name, args)

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
        if self.current >= len(self.tokens):
            return False
        return self.tokens[self.current].type == typ

    def _advance(self):
        self.current += 1
        return self.tokens[self.current - 1]

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _is_at_end(self):
        return self._peek().type == TokenType.EOF