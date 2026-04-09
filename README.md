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
