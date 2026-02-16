# MiniCompiler

Упрощённый компилятор C-подобного языка → x86-64 ASM.

**Спринт 1:** Лексический анализатор (полностью выполнен по требованиям).

## Быстрый старт (PowerShell)

```powershell
pip install -e .
minicompiler lex examples\hello.mc --output tokens.txt
Структура проекта
```

src/lexer/ — токены и сканер
tests/ — тесты
docs/language_spec.md — спецификация
