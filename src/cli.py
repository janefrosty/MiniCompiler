import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from error import print_error, print_warning

DEFAULT_CONFIG = {
    "optimize": 0,
    "target": "x86_64",
    "emit": "asm",  # asm, obj, exe
    "output": None,
    "stop_after": None,  # lex, parse, semantic, ir, asm
    "verbose": False,
}

def load_config() -> Dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    
    home_config = Path.home() / ".minicc" / "config.json"
    project_config = Path.cwd() / ".minicc" / "config.json"
    for cfg_path in [home_config, project_config]:
        if cfg_path.exists():
            try:
                with open(cfg_path, 'r') as f:
                    user_cfg = json.load(f)
                    config.update(user_cfg)
            except Exception:
                pass
    
    env_opts = os.environ.get("MINIC_OPTIONS", "")
    if env_opts:
        pass
    
    return config

def parse_arguments() -> argparse.Namespace:
    """Разбирает аргументы командной строки с учётом конфигурации."""
    config = load_config()
    
    parser = argparse.ArgumentParser(
        description="MiniCompiler - компилятор языка MiniLang (Sprint 8)",
        epilog="Пример: minicompiler -S -O2 examples/demo.mc -o demo.s"
    )
    
    # Режимы компиляции (группа)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("-E", action="store_true", help="Остановиться после препроцессинга")
    mode_group.add_argument("-S", action="store_true", help="Генерировать ассемблерный код, не выполнять ассемблирование")
    mode_group.add_argument("-c", action="store_true", help="Компилировать в объектный файл")
    
    # Выходной файл
    parser.add_argument("-o", "--output", help="Выходной файл")
    
    # Опции отладки/просмотра
    parser.add_argument("--ast", action="store_true", help="Вывести AST и остановиться")
    parser.add_argument("--ir", action="store_true", help="Вывести IR и остановиться")
    parser.add_argument("--tokens", action="store_true", help="Вывести токены и остановиться")
    
    # Уровни оптимизации
    parser.add_argument("-O", "--optimize", type=int, choices=[0,1,2,3], default=config.get("optimize", 0),
                        help="Уровень оптимизации (0-3)")
    
    # Целевая архитектура
    parser.add_argument("--target", default=config.get("target", "x86_64"),
                        help="Целевая архитектура (сейчас только x86_64)")
    
    # Дополнительные флаги
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    parser.add_argument("--version", action="store_true", help="Показать версию компилятора")
    
    # Входной файл (позиционный)
    parser.add_argument("input", nargs="?", help="Входной файл")
    
    args = parser.parse_args()
    
    # Наложение конфига (уже сделано через defaults)
    return args