import sys
from typing import Optional

COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'reset': '\033[0m',
}

def supports_color() -> bool:
    """Проверяет, поддерживает ли терминал цвета."""
    if not sys.stdout.isatty():
        return False
    if sys.platform == 'win32':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except:
            return False
    return True

_color_enabled = supports_color()

def colorize(text: str, color: str) -> str:
    """Оборачивает текст в ANSI-код цвета, если включён."""
    if not _color_enabled:
        return text
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"

def print_error(
    message: str,
    filepath: Optional[str] = None,
    line: Optional[int] = None,
    column: Optional[int] = None,
    source_line: Optional[str] = None,
    hint: Optional[str] = None,
    error_code: str = "E000"
):
    """
    Печатает форматированную ошибку с контекстом.
    """
    header = colorize(f"{error_code}: {message}", "red")
    if filepath and line and column:
        location = colorize(f"{filepath}:{line}:{column}", "bold")
        print(f"{location}: {header}", file=sys.stderr)
    else:
        print(f"{colorize('error:', 'red')} {header}", file=sys.stderr)
    
    if source_line and line and column:
        print(f"    {line} | {source_line.rstrip()}", file=sys.stderr)
        caret = " " * (len(str(line)) + 3 + column - 1) + colorize("^", "green")
        print(caret, file=sys.stderr)
    
    if hint:
        print(f"{colorize('note:', 'blue')} {hint}", file=sys.stderr)
    
    print(file=sys.stderr)

def print_warning(
    message: str,
    filepath: Optional[str] = None,
    line: Optional[int] = None,
    column: Optional[int] = None,
    hint: Optional[str] = None
):
    """Печатает предупреждение."""
    header = colorize(f"warning: {message}", "yellow")
    if filepath and line and column:
        print(f"{filepath}:{line}:{column}: {header}", file=sys.stderr)
    else:
        print(header, file=sys.stderr)
    if hint:
        print(f"{colorize('note:', 'blue')} {hint}", file=sys.stderr)