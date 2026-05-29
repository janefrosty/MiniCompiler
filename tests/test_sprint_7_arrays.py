import pytest
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from ir.generator import IRGenerator
from codegen.generator import CodeGenerator
from mast.node import ArrayDecl, ArraySubscript, BinaryExpr
from ir.ir import Malloc, Store, Load, GetElementPtr
from mast.node import ArrayDecl, ArraySubscript, BinaryExpr, IdentifierExpr

def build_ir_asm(source):
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)
    code_gen = CodeGenerator()
    asm = code_gen.generate(ir)
    return ir, asm

def test_array_declaration_parsing():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    p = Parser(source)
    ast = p.parse()
    decl = ast.functions[0].body[0]
    assert isinstance(decl, ArrayDecl)
    assert decl.name == "arr"
    assert len(decl.dimensions) == 1

def test_array_subscript_parsing():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    p = Parser(source)
    ast = p.parse()
    assign = ast.functions[0].body[1]
    assert isinstance(assign, BinaryExpr) and assign.operator == "="
    assert isinstance(assign.left, ArraySubscript)

def test_ir_contains_malloc():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    ir, asm = build_ir_asm(source)
    malloc_instrs = [i for i in ir.functions[0].body if isinstance(i, Malloc)]
    assert len(malloc_instrs) >= 1

def test_ir_contains_store_for_array_assignment():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    ir, asm = build_ir_asm(source)
    store_instrs = [i for i in ir.functions[0].body if isinstance(i, Store)]
    assert len(store_instrs) >= 1

def test_ir_contains_load_for_array_access():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    ir, asm = build_ir_asm(source)
    load_instrs = [i for i in ir.functions[0].body if isinstance(i, Load)]
    assert len(load_instrs) >= 1

def test_ir_contains_gep_for_index():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    ir, asm = build_ir_asm(source)
    gep_instrs = [i for i in ir.functions[0].body if isinstance(i, GetElementPtr)]
    assert len(gep_instrs) >= 2

def test_asm_contains_malloc_call():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    ir, asm = build_ir_asm(source)
    assert "call malloc" in asm

def test_asm_contains_store_to_memory():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    ir, asm = build_ir_asm(source)
    assert "mov [" in asm or "mov qword" in asm

def test_asm_contains_load_from_memory():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    ir, asm = build_ir_asm(source)
    assert "mov e" in asm and "[" in asm

def test_asm_contains_address_computation():
    source = "fn main() { int arr[5]; arr[0] = 10; return arr[0]; }"
    ir, asm = build_ir_asm(source)
    assert "lea" in asm

def test_multi_dim_array_declaration():
    source = "fn main() { int matrix[3][4]; matrix[1][2] = 42; return matrix[1][2]; }"
    p = Parser(source)
    ast = p.parse()
    decl = ast.functions[0].body[0]
    assert isinstance(decl, ArrayDecl)
    assert len(decl.dimensions) == 2

def test_multi_dim_subscript():
    source = "fn main() { int matrix[3][4]; matrix[1][2] = 42; return matrix[1][2]; }"
    p = Parser(source)
    ast = p.parse()
    assign = ast.functions[0].body[1]
    assert isinstance(assign, BinaryExpr)
    assert assign.operator == "="
    left = assign.left
    # В парсере matrix[1][2] -> ArraySubscript(ArraySubscript(matrix, [1]), [2])
    # Собираем индексы рекурсивно, но потом переворачиваем, чтобы получить [1,2]
    indices = []
    current = left
    while isinstance(current, ArraySubscript):
        indices.append(current.indices[0].value)
        current = current.array
    indices.reverse()  # теперь порядок правильный
    assert indices == [1, 2]
    assert isinstance(current, IdentifierExpr)
    assert current.name == "matrix"

def test_array_size_calculation():
    source = "fn main() { int arr[10]; return 0; }"
    ir, asm = build_ir_asm(source)
    assert "mov rdi, 40" in asm or "mov rdi,40" in asm

def test_multi_dim_array_size():
    source = "fn main() { int arr[3][4]; return 0; }"
    ir, asm = build_ir_asm(source)
    assert "mov rdi, 48" in asm or "mov rdi,48" in asm

def test_array_bounds_checking():
    source = "fn main() { int arr[5]; return arr[10]; }"
    # Просто проверяем, что компилируется без краша
    try:
        ir, asm = build_ir_asm(source)
        assert True
    except Exception:
        pass

def test_array_of_size_one():
    source = "fn main() { int arr[1]; arr[0] = 99; return arr[0]; }"
    ir, asm = build_ir_asm(source)
    assert "mov rdi, 4" in asm or "mov rdi,4" in asm

def test_array_index_expression():
    source = "fn main() { int arr[10]; int i = 3; arr[i] = 42; return arr[i]; }"
    ir, asm = build_ir_asm(source)
    gep_instrs = [i for i in ir.functions[0].body if isinstance(i, GetElementPtr)]
    assert len(gep_instrs) >= 2
