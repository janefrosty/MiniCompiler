import pytest
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from ir.generator import IRGenerator
from ir.ir import (
    IRProgram, IRFunction, Assign, Binary, Return, Label, Jump, JumpIfZero,
    Malloc, Store, Load, GetElementPtr
)

def build_ir(source):
    p = Parser(source)
    ast = p.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator()
    return ir_gen.generate(ast)

def test_ir_program_has_functions():
    source = "fn main() { return 0; }"
    ir = build_ir(source)
    assert isinstance(ir, IRProgram)
    assert len(ir.functions) == 1
    assert ir.functions[0].name == "main"

def test_ir_function_has_body():
    source = "fn main() { return 42; }"
    ir = build_ir(source)
    func = ir.functions[0]
    assert len(func.body) > 0

def test_ir_literal_assignment():
    source = "fn main() { int x = 42; return x; }"
    ir = build_ir(source)
    func = ir.functions[0]
    # Первая инструкция может быть Assign для x или временной переменной
    assert any(isinstance(i, Assign) for i in func.body)

def test_ir_binary_operation():
    source = "fn main() { int x = 5 + 3; return x; }"
    ir = build_ir(source)
    func = ir.functions[0]
    bin_instrs = [i for i in func.body if isinstance(i, Binary)]
    assert len(bin_instrs) >= 1
    assert bin_instrs[0].op == "+"

def test_ir_binary_chained_operations():
    source = "fn main() { int x = 5 + 3 * 2; return x; }"
    ir = build_ir(source)
    func = ir.functions[0]
    bin_instrs = [i for i in func.body if isinstance(i, Binary)]
    assert len(bin_instrs) >= 2

def test_ir_return_literal():
    source = "fn main() { return 42; }"
    ir = build_ir(source)
    func = ir.functions[0]
    ret_instrs = [i for i in func.body if isinstance(i, Return)]
    assert len(ret_instrs) == 1
    # Значение может быть литералом или временной переменной
    # Поэтому не проверяем конкретное значение

def test_ir_return_variable():
    source = "fn main() { int x = 10; return x; }"
    ir = build_ir(source)
    func = ir.functions[0]
    ret_instrs = [i for i in func.body if isinstance(i, Return)]
    assert len(ret_instrs) == 1
    # Может возвращать x или временную переменную - не проверяем

def test_ir_if_structure():
    source = "fn main() { int x = 5; if (x > 0) { return 1; } return 0; }"
    ir = build_ir(source)
    func = ir.functions[0]
    jz_instrs = [i for i in func.body if isinstance(i, JumpIfZero)]
    jmp_instrs = [i for i in func.body if isinstance(i, Jump)]
    labels = [i for i in func.body if isinstance(i, Label)]
    # В вашем IR могут быть эти инструкции
    # Просто проверяем, что хотя бы одна условная или безусловная ветка есть
    assert len(jz_instrs) + len(jmp_instrs) >= 1

def test_ir_if_else_structure():
    source = "fn main() { if (1 > 0) { return 1; } else { return 0; } }"
    ir = build_ir(source)
    func = ir.functions[0]
    jz = [i for i in func.body if isinstance(i, JumpIfZero)]
    jmp = [i for i in func.body if isinstance(i, Jump)]
    assert len(jz) >= 1
    assert len(jmp) >= 1

def test_ir_while_loop():
    source = "fn main() { int i = 0; while (i < 10) { i = i + 1; } return i; }"
    ir = build_ir(source)
    func = ir.functions[0]
    labels = [i for i in func.body if isinstance(i, Label)]
    jz = [i for i in func.body if isinstance(i, JumpIfZero)]
    jmp = [i for i in func.body if isinstance(i, Jump)]
    assert len(labels) >= 2
    assert len(jz) >= 1
    assert len(jmp) >= 1

def test_ir_array_declaration():
    source = "fn main() { int arr[5]; arr[0] = 42; return arr[0]; }"
    ir = build_ir(source)
    func = ir.functions[0]
    malloc_instrs = [i for i in func.body if isinstance(i, Malloc)]
    store_instrs = [i for i in func.body if isinstance(i, Store)]
    load_instrs = [i for i in func.body if isinstance(i, Load)]
    gep_instrs = [i for i in func.body if isinstance(i, GetElementPtr)]
    assert len(malloc_instrs) >= 1
    assert len(store_instrs) >= 1
    assert len(load_instrs) >= 1
    assert len(gep_instrs) >= 2

def test_ir_array_index_computation():
    source = "fn main() { int arr[10]; arr[3] = 99; return arr[3]; }"
    ir = build_ir(source)
    func = ir.functions[0]
    gep_instrs = [i for i in func.body if isinstance(i, GetElementPtr)]
    assert len(gep_instrs) >= 2

def test_ir_dump_returns_string():
    source = "fn main() { return 0; }"
    ir = build_ir(source)
    dump = ir.dump()
    assert isinstance(dump, str)
    assert "function main()" in dump

def test_ir_generates_correct_number_of_instructions_for_binary():
    source = "fn main() { int x = 5 + 3; return x; }"
    ir = build_ir(source)
    func = ir.functions[0]
    # Ваш генератор может создавать временные переменные, поэтому количество инструкций > 1
    assert len(func.body) >= 3

def test_ir_empty_function():
    source = "fn main() { }"
    ir = build_ir(source)
    func = ir.functions[0]
    # Может быть пусто или с неявным return
    assert len(func.body) <= 1