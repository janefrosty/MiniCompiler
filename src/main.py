import argparse
from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from mast.node import print_ast
from ir.generator import IRGenerator
from ir.ir import IRProgram

def main():
    parser = argparse.ArgumentParser(description='MiniCompiler CLI (Sprint 4)')
    parser.add_argument('command', choices=['lex', 'parse', 'semantic', 'ir'], help='Команда')
    parser.add_argument('input', help='Исходный файл')
    parser.add_argument('--output', '-o', help='Выходной файл')
    
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        source = f.read()
    
    if args.command == 'lex':
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        output = '\n'.join(str(t) for t in tokens)
    elif args.command == 'parse':
        p = Parser(source)
        ast_tree = p.parse()
        output = print_ast(ast_tree)
    elif args.command == 'semantic':
        p = Parser(source)
        ast_tree = p.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast_tree)
        output = print_ast(ast_tree)
    else:  # ir
        p = Parser(source)
        ast_tree = p.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast_tree)
        generator = IRGenerator()
        ir_program = generator.generate(ast_tree)
        output = ir_program.dump()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Результат сохранён в {args.output}')
    else:
        print(output)

if __name__ == '__main__':
    main()
