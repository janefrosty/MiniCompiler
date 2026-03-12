from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Node:
    pass

@dataclass
class Program(Node):
    functions: List['FunctionDecl']

@dataclass
class FunctionDecl(Node):
    name: str
    params: List[str]
    body: List['Statement']

@dataclass
class VarDecl(Node):
    name: str
    value: 'Expression'

@dataclass
class ReturnStmt(Node):
    value: 'Expression'

@dataclass
class Expression(Node):
    pass

@dataclass
class BinaryExpr(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class LiteralExpr(Expression):
    value: int | float | str | bool

@dataclass
class IdentifierExpr(Expression):
    name: str

# Для красивого вывода
def print_ast(node: Node, indent: str = '') -> str:
    if isinstance(node, Program):
        return indent + 'Program\n' + '\\n'.join(print_ast(f, indent + '  ') for f in node.functions)
    if isinstance(node, FunctionDecl):
        return indent + f'Function {node.name}({node.params})\n' + '\\n'.join(print_ast(s, indent + '  ') for s in node.body)
    if isinstance(node, VarDecl):
        return indent + f'VarDecl {node.name} = {node.value}'
    if isinstance(node, ReturnStmt):
        return indent + f'Return {node.value}'
    if isinstance(node, BinaryExpr):
        return indent + f'Binary {node.operator} ({node.left}, {node.right})'
    if isinstance(node, LiteralExpr):
        return indent + f'Literal {node.value}'
    if isinstance(node, IdentifierExpr):
        return indent + f'Identifier {node.name}'
    return indent + str(type(node))
