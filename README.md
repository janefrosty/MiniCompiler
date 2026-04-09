# MiniCompiler

Упрощённый компилятор C-подобного языка → x86-64 ASM.


## Структура проекта

src/lexer/ — токены и сканер

src/parser/ — парсер и грамматика

src/mast/ — узлы Абстрактного Синтаксического Дерева

src/semantic/ — таблица символов, проверка типов и семантический анализатор

tests/ — тесты

docs/ — спецификации языка

**Спринт 1:** Лексический анализатор.

```powershell
pip install -e .
minicompiler lex examples\hello.mc --output tokens.txt
```

<<<<<<< HEAD
=======
## Структура проекта

src/lexer/ — токены и сканер

tests/ — тесты

docs/language_spec.md — спецификация


>>>>>>> ab22e5846d93eeaf7f9faa033d6c87fe7743a5d4
**Спринт 2:** Создать парсер (рекурсивного спуска), построить чёткое AST.

```powershell
minicompiler parse examples\hello.mc --output ast.txt

Get-Content ast.txt
```

**Спринт 3:** Семантический анализ и таблица символов.

```powershell
PowerShellminicompiler semantic examples\hello.mc
```

## Тесты

```powershell
pytest tests\ -v
```
