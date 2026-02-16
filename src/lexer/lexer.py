from .token import Token, TokenType
from typing import List, Any

class Lexer:
    def __init__(self, source: str):
        # LEX-4: Удаляем BOM (UTF-8 с BOM)
        if source.startswith('\ufeff'):
            source = source[1:]
            print('ℹ️  BOM удалён из источника')
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        
        self.keywords = {
            'if': TokenType.KW_IF, 'else': TokenType.KW_ELSE,
            'while': TokenType.KW_WHILE, 'for': TokenType.KW_FOR,
            'int': TokenType.KW_INT, 'float': TokenType.KW_FLOAT,
            'bool': TokenType.KW_BOOL, 'true': TokenType.KW_TRUE,
            'false': TokenType.KW_FALSE, 'void': TokenType.KW_VOID,
            'struct': TokenType.KW_STRUCT, 'fn': TokenType.KW_FN,
            'return': TokenType.KW_RETURN,
        }
    
    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def _scan_token(self):
        c = self._advance()
        
        if c.isspace():
            if c in '\r\n':
                self._handle_newline(c)
            return
        
        # Комментарии
        if c == '/' and self._match('/'):
            while self._peek() not in '\r\n' and not self._is_at_end():
                self._advance()
            return
        if c == '/' and self._match('*'):
            self._multi_line_comment()
            return
        
        # Многосимвольные операторы
        if c == '=':
            if self._match('='): self._add_token(TokenType.EQ)
            else: self._add_token(TokenType.ASSIGN)
            return
        if c == '!':
            if self._match('='): self._add_token(TokenType.NEQ)
            else: self._add_token(TokenType.NOT)
            return
        if c == '<':
            if self._match('='): self._add_token(TokenType.LE)
            else: self._add_token(TokenType.LT)
            return
        if c == '>':
            if self._match('='): self._add_token(TokenType.GE)
            else: self._add_token(TokenType.GT)
            return
        if c == '&' and self._match('&'):
            self._add_token(TokenType.AND)
            return
        if c == '|' and self._match('|'):
            self._add_token(TokenType.OR)
            return
        
        # Числа
        if c.isdigit() or (c == '-' and self._peek().isdigit()):
            self._number()
            return
        
        # Строки
        if c == '"':
            self._string()
            return
        
        # Идентификаторы и ключевые слова
        if c.isalpha() or c == '_':
            self._identifier()
            return
        
        # Односимвольные
        single_char = {
            '(': TokenType.LPAREN, ')': TokenType.RPAREN,
            '{': TokenType.LBRACE, '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
            ';': TokenType.SEMICOLON, ',': TokenType.COMMA,
            '.': TokenType.DOT, '+': TokenType.PLUS,
            '-': TokenType.MINUS, '*': TokenType.STAR,
            '/': TokenType.SLASH, '%': TokenType.PERCENT,
        }
        if c in single_char:
            self._add_token(single_char[c])
            return
        
        # Ошибка (LEX-5)
        self._error(f"Неожиданный символ: '{c}'")
    
    # Вспомогательные методы (LEX-6: O(n))
    def _advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        self.column += 1
        return c
    
    def _peek(self) -> str:
        if self._is_at_end(): return '\0'
        return self.source[self.current]
    
    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True
    
    def _add_token(self, token_type: TokenType, literal: Any = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, self.line, self.column - len(text), literal))
    
    def _number(self):
        while self._peek().isdigit():
            self._advance()
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
            value = float(self.source[self.start:self.current])
            self._add_token(TokenType.FLOAT_LITERAL, value)
        else:
            value = int(self.source[self.start:self.current])
            self._add_token(TokenType.INT_LITERAL, value)
    
    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == '\n':
                self._handle_newline('\n')
            self._advance()
        if self._is_at_end():
            self._error('Не закрыта строка')
            return
        self._advance()
        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING_LITERAL, value)
    
    def _identifier(self):
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self._add_token(token_type)
    
    def _multi_line_comment(self):
        while not (self._peek() == '*' and self._peek_next() == '/'):
            if self._is_at_end():
                self._error('Не закрыт комментарий')
                return
            if self._peek() in '\r\n':
                self._handle_newline(self._peek())
            self._advance()
        self._advance()
        self._advance()
    
    def _handle_newline(self, c: str):
        if c == '\r' and self._peek() == '\n':
            self._advance()
        self.line += 1
        self.column = 1
    
    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def _error(self, message: str):
        print(f'Ошибка на {self.line}:{self.column}: {message}')
        self.tokens.append(Token(TokenType.ERROR, '', self.line, self.column))