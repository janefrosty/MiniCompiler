from dataclasses import dataclass
from typing import Dict, Optional, List
from .type_system import Type

@dataclass
class Symbol:
    name: str
    type: Type
    kind: str          # 'var', 'param', 'function'
    line: int
    column: int

class SymbolTable:
    """SYM-1, SYM-2: Таблица символов с вложенными областями видимости"""
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]  # глобальный scope
    
    def enter_scope(self):
        self.scopes.append({})
    
    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def insert(self, name: str, symbol: Symbol) -> bool:
        """Возвращает False если дубликат в текущем scope"""
        current = self.scopes[-1]
        if name in current:
            return False
        current[name] = symbol
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Поиск от текущего scope к внешним (SYM-1)"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Только текущий scope"""
        return self.scopes[-1].get(name)
    
    def dump(self) -> str:
        """Красивый вывод таблицы символов"""
        result = []
        for i, scope in enumerate(self.scopes):
            result.append(f"Scope {i}:")
            for name, sym in scope.items():
                result.append(f"  {name}: {sym.type} ({sym.kind}) at {sym.line}:{sym.column}")
        return '\n'.join(result)
