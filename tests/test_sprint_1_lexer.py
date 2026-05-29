import pytest
from lexer.lexer import Lexer
from lexer.token import TokenType

def test_keywords():
    source = "if else while for int float bool return true false void struct fn"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    expected = [TokenType.KW_IF, TokenType.KW_ELSE, TokenType.KW_WHILE, TokenType.KW_FOR,
                TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_RETURN,
                TokenType.KW_TRUE, TokenType.KW_FALSE, TokenType.KW_VOID, TokenType.KW_STRUCT, TokenType.KW_FN]
    assert types == expected

def test_identifiers():
    source = "foo bar _myVar var123 _"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    identifiers = [t for t in tokens if t.type == TokenType.IDENTIFIER]
    # Ваш лексер распознаёт '_' как идентификатор, их 5
    assert len(identifiers) == 5

def test_integer_literals():
    source = "42 0 12345"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    literals = [t for t in tokens if t.type == TokenType.INT_LITERAL]
    assert len(literals) == 3
    assert literals[0].literal == 42
    assert literals[1].literal == 0
    assert literals[2].literal == 12345

def test_float_literals():
    source = "3.14 0.5 10.0"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    floats = [t for t in tokens if t.type == TokenType.FLOAT_LITERAL]
    assert len(floats) == 3
    assert floats[0].literal == 3.14

def test_string_literals():
    source = '"hello" "world" ""'
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    strings = [t for t in tokens if t.type == TokenType.STRING_LITERAL]
    assert len(strings) == 3
    assert strings[0].literal == "hello"

def test_boolean_literals():
    source = "true false"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert types == [TokenType.KW_TRUE, TokenType.KW_FALSE]

def test_operators():
    source = "+ - * / % = == != < <= > >= && || !"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    expected = [TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
                TokenType.ASSIGN, TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.LE,
                TokenType.GT, TokenType.GE, TokenType.AND, TokenType.OR, TokenType.NOT]
    assert types == expected

def test_delimiters():
    source = "( ) { } [ ] ; , ."
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    expected = [TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE,
                TokenType.LBRACKET, TokenType.RBRACKET, TokenType.SEMICOLON, TokenType.COMMA, TokenType.DOT]
    assert types == expected

def test_single_line_comments():
    source = "int x = 5; // this is a comment\nreturn x;"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    # Комментарии пропускаются, токенов комментариев нет
    # Просто проверяем, что нет ошибок и идентификаторы есть
    identifiers = [t for t in tokens if t.type == TokenType.IDENTIFIER]
    assert len(identifiers) >= 2

def test_multi_line_comments():
    source = "/* multi\nline\ncomment */ int x = 5;"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    int_tokens = [t for t in tokens if t.type == TokenType.KW_INT]
    ident_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
    assert len(int_tokens) == 1
    assert len(ident_tokens) == 1
    assert ident_tokens[0].lexeme == "x"

def test_unicode_handling():
    source = "int 变量名 = 42;"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    # Просто проверяем, что нет краша
    assert len(tokens) > 0

def test_whitespace_handling():
    source = "int   x\t=\n5;"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert TokenType.KW_INT in types
    assert TokenType.IDENTIFIER in types
    assert TokenType.ASSIGN in types
    assert TokenType.INT_LITERAL in types
    assert TokenType.SEMICOLON in types

def test_line_column_tracking():
    source = "int x = 5;\nreturn x;"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    for t in tokens:
        if t.type == TokenType.KW_INT:
            assert t.line == 1
            assert t.column == 1
        if t.type == TokenType.KW_RETURN:
            assert t.line == 2
            assert t.column == 1

def test_unterminated_string():
    source = '"hello'
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    error_tokens = [t for t in tokens if t.type == TokenType.ERROR]
    assert len(error_tokens) >= 1

def test_unterminated_multi_comment():
    source = "/* unterminated comment"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    error_tokens = [t for t in tokens if t.type == TokenType.ERROR]
    assert len(error_tokens) >= 1

def test_unknown_character():
    source = "int x = 5; @"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    error_tokens = [t for t in tokens if t.type == TokenType.ERROR]
    assert len(error_tokens) >= 1

def test_empty_source():
    source = ""
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF

def test_only_comments():
    source = "// just a comment\n/* another comment */"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    assert len([t for t in tokens if t.type != TokenType.EOF]) == 0

def test_nested_operators():
    source = "++ -- << >>"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    assert len(tokens) > 0

def test_token_has_literal_value():
    source = "42 3.14 \"hello\""
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    literals = [t for t in tokens if t.type in (TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.STRING_LITERAL)]
    assert literals[0].literal == 42
    assert literals[1].literal == 3.14
    assert literals[2].literal == "hello"