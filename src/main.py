import argparse
from lexer.lexer import Lexer
from parser.parser import Parser
from mast.node import print_ast

def main():
    parser = argparse.ArgumentParser(description='MiniCompiler CLI (Sprint 2)')
    parser.add_argument('command', choices=['lex', 'parse'], help='Команда')
    parser.add_argument('input', help='Исходный файл')
    parser.add_argument('--output', '-o', help='Выходной файл')
    
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        source = f.read()
    
    if args.command == 'lex':
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        output = '\n'.join(str(t) for t in tokens)
    else:  # parse
        p = Parser(source)
        ast_tree = p.parse()
        output = print_ast(ast_tree)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'✅ Результат сохранён в {args.output}')
    else:
        print(output)

if __name__ == '__main__':
    main()
