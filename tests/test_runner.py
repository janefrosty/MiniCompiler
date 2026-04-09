import pytest
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from mast.node import Program
from semantic.errors import SemanticError

def test_valid_main_with_return():
    source = 'fn main() { int x = 42; return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    assert len(analyzer.errors) == 0

def test_undeclared_variable():
    source = 'fn main() { return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError):
        analyzer.analyze(ast)

def test_redeclared_variable():
    source = 'fn main() { int x = 1; int x = 2; return 0; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError):
        analyzer.analyze(ast)

def test_bool_literals_supported():
    source = 'fn main() { int x = 1; return true; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    assert len(analyzer.errors) == 0
