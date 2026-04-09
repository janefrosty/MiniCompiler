from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional

class TokenType(Enum):
    KW_IF = auto()
    KW_ELSE = auto()
    KW_WHILE = auto()
    KW_FOR = auto()
    KW_INT = auto()
    KW_FLOAT = auto()
    KW_BOOL = auto()
    KW_TRUE = auto()
    KW_FALSE = auto()
    KW_VOID = auto()
    KW_STRUCT = auto()
    KW_FN = auto()
    KW_RETURN = auto()
    
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOL_LITERAL = auto()
    
    IDENTIFIER = auto()
    
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    ASSIGN = auto()
    
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    ARROW = auto()
    
    EOF = auto()
    ERROR = auto()

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
    literal: Optional[Any] = None
    
    def __str__(self) -> str:
        val = f' {self.literal}' if self.literal is not None else ''
        return f'{self.line}:{self.column} {self.type.name} \"{self.lexeme}\"{val}'
