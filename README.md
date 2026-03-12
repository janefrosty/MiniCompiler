# MiniCompiler

Упрощённый компилятор C-подобного языка → x86-64 ASM.

**Спринт 1:** Лексический анализатор.

```powershell
pip install -e .
minicompiler lex examples\hello.mc --output tokens.txt
```

## Структура проекта

src/lexer/ — токены и сканер

tests/ — тесты

docs/language_spec.md — спецификация


**Спринт 2:** Создать парсер (рекурсивного спуска), построить чёткое AST.

```powershell
minicompiler parse examples\hello.mc --output ast.txt

Get-Content ast.txt
```

## Тесты

```powershell
pytest tests\ -v
```
