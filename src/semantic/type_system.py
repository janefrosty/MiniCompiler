from dataclasses import dataclass
from typing import Dict, Optional

@dataclass(frozen=True)
class Type:
    name: str

    def __str__(self):
        return self.name

# Базовые типы (SYM-4)
INT_TYPE = Type('int')
FLOAT_TYPE = Type('float')
BOOL_TYPE = Type('bool')
VOID_TYPE = Type('void')
STRING_TYPE = Type('string')   # для будущего

class FunctionType(Type):
    def __init__(self, return_type: Type, param_types: list[Type]):
        super().__init__(f'fn({param_types}) -> {return_type}')
        self.return_type = return_type
        self.param_types = param_types

class StructType(Type):
    def __init__(self, name: str, fields: Dict[str, Type]):
        super().__init__(name)
        self.fields = fields

# Проверка совместимости типов
def is_compatible(actual: Type, expected: Type) -> bool:
    if actual == expected:
        return True
    if actual == INT_TYPE and expected == FLOAT_TYPE:
        return True  # int можно присвоить float
    return False

def get_binary_result_type(left: Type, op: str, right: Type) -> Optional[Type]:
    if left == INT_TYPE and right == INT_TYPE:
        return INT_TYPE
    if left == FLOAT_TYPE or right == FLOAT_TYPE:
        return FLOAT_TYPE
    if op in ('==', '!=') and left == right:
        return BOOL_TYPE
    return None
