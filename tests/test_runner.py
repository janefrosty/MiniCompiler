import pytest
from parser.parser import Parser
from mast.node import Program

def test_simple_function():
    source = 'fn main() { int x = 42; return x; }'
    p = Parser(source)
    ast_tree = p.parse()
    assert isinstance(ast_tree, Program)
    assert len(ast_tree.functions) == 1
    assert ast_tree.functions[0].name == 'main'

print('✅ Тесты Sprint 2 готовы')
