from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Node: pass

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
class ArrayDecl(Node):
    name: str
    dimensions: List['Expression'] 
    initializer: Optional[List['Expression']] = None  

@dataclass
class ReturnStmt(Node):
    value: 'Expression'

@dataclass
class IfStmt(Node):
    condition: 'Expression'
    then_body: List['Statement']
    else_body: Optional[List['Statement']] = None

@dataclass
class WhileStmt(Node):
    condition: 'Expression'
    body: List['Statement']

@dataclass
class CallExpr(Node):
    name: str
    args: List['Expression']

@dataclass
class Expression(Node): pass

@dataclass
class BinaryExpr(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class LiteralExpr(Expression):
    value: int | bool

@dataclass
class IdentifierExpr(Expression):
    name: str

@dataclass
class ArraySubscript(Expression):
    array: Expression
    indices: List['Expression']

def print_ast(node: Node, indent: str = '') -> str:
    if isinstance(node, Program):
        return indent + 'Program\n' + '\n'.join(print_ast(f, indent + '  ') for f in node.functions)
    if isinstance(node, FunctionDecl):
        return indent + f'Function {node.name}\n' + '\n'.join(print_ast(s, indent + '  ') for s in node.body)
    if isinstance(node, VarDecl):
        return indent + f'VarDecl {node.name} = {node.value}'
    if isinstance(node, ArrayDecl):
        dims_str = ', '.join(str(d) for d in node.dimensions)
        return indent + f'ArrayDecl {node.name}[{dims_str}]'
    if isinstance(node, CallExpr):
        return indent + f'Call {node.name}({node.args})'
    if isinstance(node, IfStmt):
        return indent + f'If ({node.condition})'
    if isinstance(node, WhileStmt):
        return indent + f'While ({node.condition})'
    if isinstance(node, ArraySubscript):
        indices_str = ', '.join(str(i) for i in node.indices)
        return indent + f'ArraySubscript {node.array}[{indices_str}]'
    return indent + str(type(node))