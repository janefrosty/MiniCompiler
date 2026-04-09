import pytest
from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from ir.generator import IRGenerator
from semantic.errors import SemanticError
from mast.node import Program


def test_lexer_and_parser_basic():
    source = 'fn main() { int x = 42; return x; }'
    # Lexer
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    assert len(tokens) > 10
    assert any(t.type.name == 'KW_FN' for t in tokens)
    
    # Parser
    p = Parser(source)
    ast = p.parse()
    assert isinstance(ast, Program)
    assert len(ast.functions) == 1
    assert ast.functions[0].name == 'main'


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
    source = 'fn main() { return true; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    assert len(analyzer.errors) == 0


def test_valid_ir_generation():
    source = 'fn main() { int x = 42; return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    generator = IRGenerator()
    ir = generator.generate(ast)
    assert len(ir.functions) == 1
    assert ir.functions[0].name == 'main'

def test_ir_with_binary_expression():
    source = 'fn main() { int x = 10 + 20; return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    generator = IRGenerator()
    ir = generator.generate(ast)
    assert any('+' in str(instr) for instr in ir.functions[0].body)

