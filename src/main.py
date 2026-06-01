#!/usr/bin/env python3
"""
MiniCompiler - кросс-платформенная сборка через NASM + GoLink (Windows) или ld (Linux/macOS).
"""

import argparse
import subprocess
import sys
import shutil
import os
from pathlib import Path

from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from ir.generator import IRGenerator
from codegen.generator import CodeGenerator
from mast.node import print_ast
from error import print_error, print_warning

# ------------------------------------------------------------
# Вспомогательные функции
# ------------------------------------------------------------
def read_source(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return f.read()
    except FileNotFoundError:
        print_error(f"Файл '{filepath}' не найден")
        sys.exit(1)
    except Exception as e:
        print_error(f"Ошибка чтения файла: {e}")
        sys.exit(1)

def find_real_tool(name: str) -> Path | None:
    """
    Ищет настоящий исполняемый файл (не Python-скрипт).
    Сначала в папке tools/ проекта, затем в PATH.
    """
    proj_dir = Path(__file__).parent.parent
    tools_dir = proj_dir / "tools"

    # Поиск в tools/ (с учётом расширений)
    if sys.platform == "win32":
        candidates = [tools_dir / f"{name}.exe", tools_dir / name]
    else:
        candidates = [tools_dir / name]
    for cand in candidates:
        if cand.exists() and cand.is_file():
            return cand

    # Поиск в PATH
    for p in os.environ.get("PATH", "").split(os.pathsep):
        p = Path(p)
        if sys.platform == "win32":
            exe = p / f"{name}.exe"
            if exe.exists() and exe.is_file():
                # Небольшая проверка, что это не python-скрипт-обёртка
                try:
                    with open(exe, 'rb') as f:
                        header = f.read(2)
                        if header == b'MZ':  # PE-исполнимый
                            return exe
                except:
                    pass
        else:
            bin_path = p / name
            if bin_path.exists() and bin_path.is_file():
                try:
                    with open(bin_path, 'rb') as f:
                        if f.read(2) == b'#!':  # скрипт
                            continue
                except:
                    pass
                return bin_path
    return None

def build_exe(asm_path: Path, output_exe: Path):
    """Собирает исполняемый файл."""
    nasm = find_real_tool('nasm')
    if not nasm:
        print_error("NASM не найден", hint="Скачайте nasm.exe и положите в tools/")
        sys.exit(1)

    if sys.platform == 'win32':
        obj_format = 'win64'
        obj_ext = '.obj'
    else:
        obj_format = 'elf64'
        obj_ext = '.o'

    obj_path = asm_path.with_suffix(obj_ext)

    # Ассемблирование
    try:
        subprocess.run([str(nasm), '-f', obj_format, str(asm_path), '-o', str(obj_path)], check=True)
    except subprocess.CalledProcessError:
        print_error("Ошибка ассемблирования")
        sys.exit(1)

    # Линковка
    if sys.platform == 'win32':
        golink = find_real_tool('golink')
        if not golink:
            print_error("GoLink не найден", hint="Скачайте golink.exe и положите в tools/ (переименуйте в golink.exe)")
            sys.exit(1)
        # GoLink: /console, /entry main, объектный файл, библиотеки, /fo out.exe
        try:
            subprocess.run([
                str(golink),
                '/console',
                '/entry', 'main',
                str(obj_path),
                'kernel32.dll',
                'msvcrt.dll',
                '/fo', str(output_exe)
            ], check=True)
        except subprocess.CalledProcessError:
            print_error("Ошибка линковки (GoLink)")
            sys.exit(1)
    else:
        ld = shutil.which('ld')
        if not ld:
            print_error("ld не найден", hint="Установите binutils")
            sys.exit(1)
        try:
            subprocess.run([ld, '-o', str(output_exe), str(obj_path), '-lc'], check=True)
        except subprocess.CalledProcessError:
            print_error("Ошибка линковки (ld)")
            sys.exit(1)

    print(f"Исполняемый файл создан: {output_exe}")

def build_obj(asm_path: Path, output_obj: Path):
    """Собирает объектный файл."""
    nasm = find_real_tool('nasm')
    if not nasm:
        print_error("NASM не найден")
        sys.exit(1)

    if sys.platform == 'win32':
        obj_format = 'win64'
    else:
        obj_format = 'elf64'

    try:
        subprocess.run([str(nasm), '-f', obj_format, str(asm_path), '-o', str(output_obj)], check=True)
    except subprocess.CalledProcessError:
        print_error("Ошибка ассемблирования")
        sys.exit(1)
    print(f"Объектный файл создан: {output_obj}")

# ------------------------------------------------------------
# Основная функция
# ------------------------------------------------------------
def main():
    # Обработка старого стиля команд (lex, parse, semantic, ir, asm)
    if len(sys.argv) > 1 and sys.argv[1] in ('lex', 'parse', 'semantic', 'ir', 'asm'):
        old_parser = argparse.ArgumentParser(description='MiniCompiler CLI (Sprint 6)')
        old_parser.add_argument('command', choices=['lex', 'parse', 'semantic', 'ir', 'asm'])
        old_parser.add_argument('input')
        old_parser.add_argument('--output', '-o', help='Выходной файл')
        old_args = old_parser.parse_args()

        source = read_source(old_args.input)

        if old_args.command == 'lex':
            lexer = Lexer(source)
            tokens = lexer.scan_tokens()
            output = '\n'.join(str(t) for t in tokens)
        elif old_args.command == 'parse':
            p = Parser(source)
            ast_tree = p.parse()
            output = print_ast(ast_tree)
        elif old_args.command == 'semantic':
            p = Parser(source)
            ast_tree = p.parse()
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast_tree)
            output = print_ast(ast_tree)
        elif old_args.command == 'ir':
            p = Parser(source)
            ast_tree = p.parse()
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast_tree)
            ir_gen = IRGenerator()
            ir_program = ir_gen.generate(ast_tree)
            output = ir_program.dump()
        else:  # asm
            p = Parser(source)
            ast_tree = p.parse()
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast_tree)
            ir_gen = IRGenerator()
            ir_program = ir_gen.generate(ast_tree)
            code_gen = CodeGenerator()
            output = code_gen.generate(ir_program)

        if old_args.output:
            with open(old_args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f'Результат сохранён в {old_args.output}')
        else:
            print(output)
        return

    # ----- Новый стиль -----
    parser = argparse.ArgumentParser(
        description="MiniCompiler v0.8 (Sprint 8)",
        epilog="Примеры:\n"
               "  minicompiler -S file.mc -o file.s          # только ассемблер\n"
               "  minicompiler -c file.mc -o file.o          # объектный файл\n"
               "  minicompiler file.mc -o file.exe           # исполняемый файл\n"
               "Требуется NASM и GoLink (Windows) или ld (Linux/macOS)."
    )
    parser.add_argument('-S', action='store_true', help='Только ассемблер')
    parser.add_argument('-c', action='store_true', help='Только объектный файл')
    parser.add_argument('-E', action='store_true', help='Только препроцессинг (заглушка)')
    parser.add_argument('--ast', action='store_true', help='Вывести AST')
    parser.add_argument('--ir', action='store_true', help='Вывести IR')
    parser.add_argument('--tokens', action='store_true', help='Вывести токены')
    parser.add_argument('-o', '--output', help='Выходной файл')
    parser.add_argument('-O', '--optimize', type=int, choices=[0,1,2,3], default=0, help='Оптимизация')
    parser.add_argument('--target', default='x86_64', help='Цель')
    parser.add_argument('-v', '--verbose', action='store_true', help='Подробно')
    parser.add_argument('--version', action='store_true', help='Версия')
    parser.add_argument('input', nargs='?', help='Входной файл')

    args = parser.parse_args()

    if args.version:
        print("MiniCompiler v0.8 (Sprint 8) — кросс-платформенная сборка")
        sys.exit(0)

    if not args.input:
        print_error("Не указан входной файл")
        sys.exit(1)

    source = read_source(args.input)

    if args.tokens:
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        for t in tokens:
            print(t)
        sys.exit(0)

    try:
        p = Parser(source)
        ast = p.parse()
    except Exception as e:
        print_error(str(e), filepath=args.input)
        sys.exit(1)

    if args.ast:
        print(print_ast(ast))
        sys.exit(0)

    try:
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
    except Exception:
        sys.exit(1)

    ir_gen = IRGenerator()
    ir = ir_gen.generate(ast)

    if args.ir:
        print(ir.dump())
        sys.exit(0)

    code_gen = CodeGenerator()
    asm = code_gen.generate(ir)

    # Определяем выходной файл
    if args.output:
        out_path = Path(args.output)
    else:
        base = Path(args.input).stem
        out_path = Path(f"{base}.s")

    ext = out_path.suffix.lower()

    if args.S:
        # только ассемблер
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(asm)
        print(f"Ассемблер сохранён: {out_path}")
    elif args.c:
        # объектный файл
        asm_file = out_path.with_suffix('.s')
        obj_file = out_path if ext == '.o' else out_path.with_suffix('.o')
        with open(asm_file, 'w', encoding='utf-8') as f:
            f.write(asm)
        build_obj(asm_file, obj_file)
        asm_file.unlink(missing_ok=True)
    else:
        # исполняемый файл
        asm_file = out_path.with_suffix('.s')
        exe_file = out_path if (ext == '.exe' or not ext) else out_path.with_suffix('.exe')
        with open(asm_file, 'w', encoding='utf-8') as f:
            f.write(asm)
        build_exe(asm_file, exe_file)
        asm_file.unlink(missing_ok=True)

    if args.verbose:
        print(f"Оптимизация: -O{args.optimize} (заглушка)")
        print(f"Цель: {args.target}")

if __name__ == '__main__':
    main()