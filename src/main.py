import sys
import argparse
from lexer.lexer import Lexer

def main():
    parser = argparse.ArgumentParser(description="MiniCompiler CLI (Sprint 1)")
    parser.add_argument("command", choices=["lex"], help="Команда (lex)")
    parser.add_argument("input", help="Исходный файл (.mc)")
    parser.add_argument("--output", "-o", help="Выходной файл токенов")
    
    args = parser.parse_args()
    
    with open(args.input, "r", encoding="utf-8") as f:
        source = f.read()
    
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for token in tokens:
                f.write(str(token) + "\n")
        print(f"✅ Токены сохранены в {args.output}")
    else:
        for token in tokens:
            print(token)

if __name__ == "__main__":
    main()
