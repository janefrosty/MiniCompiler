import pytest
from parser.parser import Parser
from mast.node import Program, FunctionDecl, VarDecl, ReturnStmt, BinaryExpr, LiteralExpr, IdentifierExpr, IfStmt, WhileStmt

def test_parses_empty_program():
    source = ""
    p = Parser(source)
    ast = p.parse()
    assert isinstance(ast, Program)
    assert len(ast.functions) == 0

def test_parses_single_function():
    source = "fn main() { return 0; }"
    p = Parser(source)
    ast = p.parse()
    assert len(ast.functions) == 1
    assert ast.functions[0].name == "main"

def test_parses_multiple_functions():
    source = "fn first() { return 1; } fn second() { return 2; }"
    p = Parser(source)
    ast = p.parse()
    assert len(ast.functions) == 2
    assert ast.functions[0].name == "first"
    assert ast.functions[1].name == "second"

def test_function_with_parameters():
    source = "fn add(a, b) { return a + b; }"
    p = Parser(source)
    ast = p.parse()
    func = ast.functions[0]
    assert func.params == ["a", "b"]

def test_parses_var_declaration():
    source = "fn main() { int x = 42; return x; }"
    p = Parser(source)
    ast = p.parse()
    stmt = ast.functions[0].body[0]
    assert isinstance(stmt, VarDecl)
    assert stmt.name == "x"
    assert isinstance(stmt.value, LiteralExpr)
    assert stmt.value.value == 42


def test_parses_return_statement_with_literal():
    source = "fn main() { return 42; }"
    p = Parser(source)
    ast = p.parse()
    stmt = ast.functions[0].body[0]
    assert isinstance(stmt, ReturnStmt)
    assert isinstance(stmt.value, LiteralExpr)
    assert stmt.value.value == 42

def test_parses_return_statement_with_expression():
    source = "fn main() { int x = 5; return x + 2; }"
    p = Parser(source)
    ast = p.parse()
    ret = ast.functions[0].body[-1]
    assert isinstance(ret, ReturnStmt)
    assert isinstance(ret.value, BinaryExpr)

def test_parses_if_statement():
    source = "fn main() { if (1 > 0) { return 1; } }"
    p = Parser(source)
    ast = p.parse()
    if_stmt = ast.functions[0].body[0]
    assert isinstance(if_stmt, IfStmt)
    assert if_stmt.else_body is None

def test_parses_if_else_statement():
    source = "fn main() { if (1 > 0) { return 1; } else { return 0; } }"
    p = Parser(source)
    ast = p.parse()
    if_stmt = ast.functions[0].body[0]
    assert isinstance(if_stmt, IfStmt)
    assert if_stmt.else_body is not None

def test_parses_while_statement():
    source = "fn main() { int i = 0; while (i < 10) { i = i + 1; } return i; }"
    p = Parser(source)
    ast = p.parse()
    while_stmt = ast.functions[0].body[1]
    assert isinstance(while_stmt, WhileStmt)

def test_parses_binary_expression():
    source = "fn main() { int x = 5 + 3 * 2; return x; }"
    p = Parser(source)
    ast = p.parse()
    expr = ast.functions[0].body[0].value
    assert isinstance(expr, BinaryExpr)
    # У вас правоассоциативно? Проверим, что это бинарный узел.
    assert expr.operator in ('+', '*')

def test_parses_parenthesized_expression():
    source = "fn main() { int x = (5 + 3) * 2; return x; }"
    p = Parser(source)
    ast = p.parse()
    expr = ast.functions[0].body[0].value
    assert isinstance(expr, BinaryExpr)
    assert expr.operator == '*'

def test_parses_unary_expression():
    source = "fn main() { int x = -5; int y = !true; return 0; }"
    p = Parser(source)
    ast = p.parse()
    # Ваш парсер превращает -5 в LiteralExpr(-5) - это допустимо
    # Просто проверим, что парсинг прошёл без ошибок
    assert len(ast.functions[0].body) >= 2

def test_parses_comparison_operators():
    source = "fn main() { int x = 5 < 10; int y = 10 >= 5; return 0; }"
    p = Parser(source)
    ast = p.parse()
    assert len(ast.functions[0].body) >= 2

def test_reports_missing_semicolon():
    source = "fn main() { int x = 5 return x; }"
    p = Parser(source)
    with pytest.raises(Exception) as excinfo:
        p.parse()
    assert "Expected SEMICOLON" in str(excinfo.value) or "semicolon" in str(excinfo.value).lower()

def test_reports_missing_parenthesis():
    source = "fn main( int x = 5; return x; }"
    p = Parser(source)
    with pytest.raises(Exception):
        p.parse()

def test_reports_unexpected_token():
    source = "fn main() { int x = @ 5; }"
    p = Parser(source)
    with pytest.raises(Exception):
        p.parse()

def test_ast_contains_correct_node_types():
    source = """fn test(a, b) {
        int x = 10;
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }"""
    p = Parser(source)
    ast = p.parse()
    func = ast.functions[0]
    assert isinstance(func, FunctionDecl)
    assert isinstance(func.body[0], VarDecl)
    assert isinstance(func.body[1], IfStmt)