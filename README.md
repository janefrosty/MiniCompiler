# MiniCompiler

Упрощённый компилятор C-подобного языка → x86-64 ASM.

- **Спринт 1:** Лексический анализатор.  
- **Спринт 2:** Синтаксический анализ и построение AST.  
- **Спринт 3:** Семантический анализ и таблица символов.  
- **Спринт 4:** Промежуточное представление (IR) и генерация кода.  
- **Спринт 5:** Основа бэкенда x86-64 и прологи/эпилоги функций.
- **Спринт 6:** Управление потоком и сложные выражения.
- **Спринт 7:** Продвинутые возможности и оптимизации.

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
minicompiler semantic examples\hello.mc
```

**Спринт 4:** Промежуточное представление (IR) и генерация кода.

```powershell
pip install -e .
minicompiler semantic examples\hello.mc
minicompiler ir      examples\hello.mc --output ir.txt
```

**Спринт 5:** Основа бэкенда x86-64 и прологи/эпилоги функций.

```powershell
pip install -e .
minicompiler asm examples\hello.mc --output main.asm

Get-Content main.asm
```

**Спринт 6:** Управление потоком и сложные выражения.

```powershell
pip install -e .
minicompiler asm examples\while_test.mc --output while_test.asm
minicompiler asm examples\if_test.mc --output if_test.asm
Get-Content while_test.asm
Get-Content if_test.asm
```

**Спринт 7:** Продвинутые возможности и оптимизации.

```powershell
pip install -e .
minicompiler asm examples\array_test.mc --output array_test.asm
Get-Content array_test.asm
```

## Тесты

```powershell
cd tests
python run_all_tests.py

#или
cd tests
pytest test_sprint_1_lexer.py -v
#...
```


## использование

```powershell
# Установка nasm (ассемблер)
sudo apt update && sudo apt install nasm

# Установка binutils (для ld, если ещё нет)
sudo apt install binutils

cd MiniCompiler
# Установка pytest (опционально, для тестов)
pip3 install pytest
pip install -e .

minicompiler examples/array_test.mc -o array_test

./array_test

echo $?


# сборка исполняемого файла из примера с массивами
minicompiler examples/array_test.mc -o array_test.exe
.\array_test.exe
echo $LASTEXITCODE   # 30

# сборка только ассемблера
minicompiler -S examples/array_test.mc -o array_test.s

# просмотр токенов
minicompiler --tokens examples/array_test.mc

# просмотр AST
minicompiler --ast examples/array_test.mc

# просмотр IR
minicompiler --ir examples/array_test.mc
```