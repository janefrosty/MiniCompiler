from dataclasses import dataclass
from typing import Dict, Optional, List
from .type_system import Type

@dataclass
class Symbol:
    name: str
    type: Type
    kind: str    
    line: int
    column: int

class SymbolTable:
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]  
    
    def enter_scope(self):
        self.scopes.append({})
    
    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def insert(self, name: str, symbol: Symbol) -> bool:
        current = self.scopes[-1]
        if name in current:
            return False
        current[name] = symbol
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        return self.scopes[-1].get(name)
    
    def dump(self) -> str:
        result = []
        for i, scope in enumerate(self.scopes):
            result.append(f"Scope {i}:")
            for name, sym in scope.items():
                result.append(f"  {name}: {sym.type} ({sym.kind}) at {sym.line}:{sym.column}")
        return '\n'.join(result)
