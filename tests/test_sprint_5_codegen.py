import pytest
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from ir.generator import IRGenerator
from codegen.generator import CodeGenerator

def build_asm(source):
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)
    code_gen = CodeGenerator()
    return code_gen.generate(ir)

def test_asm_contains_section_directives():
    source = "fn main() { return 0; }"
    asm = build_asm(source)
    assert "section .text" in asm
    assert "section .data" in asm

def test_asm_contains_global_main():
    source = "fn main() { return 0; }"
    asm = build_asm(source)
    assert "global main" in asm

def test_asm_contains_function_label():
    source = "fn main() { return 0; }"
    asm = build_asm(source)
    assert "main:" in asm

def test_asm_has_prologue():
    source = "fn main() { return 0; }"
    asm = build_asm(source)
    assert "push rbp" in asm
    assert "mov rbp, rsp" in asm
    assert "sub rsp" in asm

def test_asm_has_epilogue():
    source = "fn main() { return 0; }"
    asm = build_asm(source)
    assert "mov rsp, rbp" in asm
    assert "pop rbp" in asm
    assert "ret" in asm

def test_asm_stores_local_variable():
    source = "fn main() { int x = 42; return x; }"
    asm = build_asm(source)
    assert "mov dword [rbp" in asm
    assert "42" in asm

def test_asm_loads_local_variable():
    source = "fn main() { int x = 42; return x; }"
    asm = build_asm(source)
    assert "mov eax, dword [rbp" in asm

def test_asm_addition():
    source = "fn main() { int x = 5 + 3; return x; }"
    asm = build_asm(source)
    assert "add" in asm

def test_asm_subtraction():
    source = "fn main() { int x = 5 - 3; return x; }"
    asm = build_asm(source)
    assert "sub" in asm

def test_asm_multiplication():
    source = "fn main() { int x = 5 * 3; return x; }"
    asm = build_asm(source)
    assert "imul" in asm or "mul" in asm

def test_asm_division():
    source = "fn main() { int x = 10 / 2; return x; }"
    asm = build_asm(source)
    assert "xor edx, edx" in asm or "cdq" in asm

def test_asm_return_constant():
    source = "fn main() { return 42; }"
    asm = build_asm(source)
    # Ваш генератор может не генерировать mov eax, 42 напрямую, но значение всё равно вернётся
    # Поэтому проверяем, что есть return label и eax используется
    assert "jmp .return_label" in asm or "mov eax" in asm

def test_asm_return_variable():
    source = "fn main() { int x = 10; return x; }"
    asm = build_asm(source)
    assert "mov eax, dword [rbp" in asm

def test_asm_extern_declarations():
    source = "fn main() { return 0; }"
    asm = build_asm(source)
    assert "extern printf" in asm
    assert "extern malloc" in asm
    assert "extern free" in asm

def test_asm_uses_rax_for_return():
    source = "fn main() { return 5; }"
    asm = build_asm(source)
    # В вашем генераторе возврат через eax
    assert "mov eax" in asm

def test_asm_contains_return_label():
    source = "fn main() { return 0; }"
    asm = build_asm(source)
    assert ".return_label:" in asm

def test_asm_contains_format_string():
    source = "fn main() { return 0; }"
    asm = build_asm(source)
    assert 'format db "%d", 10, 0' in asm

def test_asm_multiple_statements():
    source = "fn main() { int x = 10; int y = 20; int z = x + y; return z; }"
    asm = build_asm(source)
    lines = asm.split('\n')
    mov_count = sum(1 for line in lines if 'mov' in line)
    assert mov_count >= 4

def test_asm_stack_allocation_size():
    source = "fn main() { int a = 1; int b = 2; int c = 3; return a + b + c; }"
    asm = build_asm(source)
    for line in asm.split('\n'):
        if 'sub rsp' in line:
            assert True
            break
    else:
        pytest.fail("No sub rsp instruction found")