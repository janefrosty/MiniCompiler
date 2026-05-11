import pytest
from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from ir.generator import IRGenerator
from codegen.generator import CodeGenerator
from semantic.errors import SemanticError
from mast.node import Program

#  Sprint 1: Lexer 
def test_lexer_basic_tokens():
    source = 'fn main() { int x = 42 + 10; return x; }'
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    token_types = [t.type.name for t in tokens]
    assert 'KW_FN' in token_types
    assert 'IDENTIFIER' in token_types
    assert 'INT_LITERAL' in token_types
    assert 'PLUS' in token_types
    assert 'LBRACE' in token_types

#  Sprint 2: Parser + AST 
def test_parser_builds_ast():
    source = 'fn main() { int x = 42; return x; }'
    p = Parser(source)
    ast = p.parse()
    assert isinstance(ast, Program)
    assert len(ast.functions) == 1
    assert ast.functions[0].name == 'main'
    assert len(ast.functions[0].body) == 2

def test_parser_supports_bool_literals():
    source = 'fn main() { return true; }'
    p = Parser(source)
    ast = p.parse()
    assert isinstance(ast, Program)

#  Sprint 3: Semantic Analysis 
def test_semantic_valid_program():
    source = 'fn main() { int x = 42; return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    assert len(analyzer.errors) == 0

def test_semantic_undeclared_variable():
    source = 'fn main() { return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    with pytest.raises(SemanticError):
        analyzer.analyze(ast)

#  Sprint 4: IR Generation 
def test_ir_generation():
    source = 'fn main() { int x = 42; int y = x + 10; return y; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)
    assert len(ir.functions) == 1
    assert ir.functions[0].name == 'main'

def test_ir_contains_binary_operation():
    source = 'fn main() { int x = 5 + 7; return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)
    body_str = str(ir.functions[0].body)
    assert '+' in body_str

#  Sprint 5: Code Generation 
def test_codegen_produces_assembly():
    source = 'fn main() { int x = 42; return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)
    code_gen = CodeGenerator()
    asm = code_gen.generate(ir)
    assert 'push rbp' in asm
    assert 'mov rbp, rsp' in asm
    assert 'ret' in asm

def test_full_pipeline():
    source = 'fn main() { int x = 100; return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)
    code_gen = CodeGenerator()
    asm = code_gen.generate(ir)
    assert len(asm) > 100
    assert 'main:' in asm

#  Sprint 6: Control Flow 
def test_if_statement_parsing():
    source = 'fn main() { int x = 10; if (x > 5) { return 1; } return 0; }'
    p = Parser(source)
    ast = p.parse()
    assert any(isinstance(s, type(ast.functions[0].body[1])) 
            for s in ast.functions[0].body if 'IfStmt' in str(type(s)))

def test_if_with_else_parsing():
    source = 'fn main() { if (1 > 0) { return 1; } else { return 0; } }'
    p = Parser(source)
    ast = p.parse()
    assert len(ast.functions[0].body) > 0

def test_while_statement_parsing():
    source = 'fn main() { int i = 0; while (i < 10) { i = i + 1; } return i; }'
    p = Parser(source)
    ast = p.parse()
    assert any('WhileStmt' in str(type(s)) for s in ast.functions[0].body)

def test_if_in_ir_generation():
    source = 'fn main() { int x = 10; if (x > 5) { return 1; } return 0; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)
    body_str = str(ir.functions[0].body)
    assert 'jz' in body_str or 'JumpIfZero' in body_str



def test_full_control_flow_code_generation():
    source = 'fn main() { int x = 1; if (x > 0) { x = x + 5; } while (x < 20) { x = x + 1; } return x; }'
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)
    code_gen = CodeGenerator()
    asm = code_gen.generate(ir)
    assert 'je' in asm or 'jz' in asm or 'JumpIfZero' in str(ir)
    assert 'jmp' in asm or 'Jump' in str(ir)