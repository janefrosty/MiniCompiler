from lexer.lexer import TokenType
from mast.node import (
    Program, FunctionDecl, VarDecl, ReturnStmt,
    BinaryExpr, LiteralExpr, IdentifierExpr
)
from .symbol_table import SymbolTable, Symbol
from .type_system import (
    INT_TYPE, FLOAT_TYPE, BOOL_TYPE, VOID_TYPE,
    is_compatible, get_binary_result_type, FunctionType
)
from .errors import SemanticError

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: list[str] = []
        self.current_function_return_type = None
        self.current_function_name = None

    def analyze(self, program: Program):
        self.visit_program(program)
        
        if self.errors:
            for err in self.errors:
                print(f' Семантическая ошибка: {err}')
            raise SemanticError(f'Найдено {len(self.errors)} семантических ошибок')
        
        print(' Семантический анализ прошёл успешно!')
        print('\\n--- Таблица символов ---')
        print(self.symbol_table.dump())
        return program

    def visit_program(self, node: Program):
        for func in node.functions:
            self.visit_function_decl(func)

    def visit_function_decl(self, node: FunctionDecl):
        self.current_function_name = node.name
        
        if node.name == 'main':
            return_type = INT_TYPE
        else:
            return_type = VOID_TYPE   
        
        func_type = FunctionType(return_type, [INT_TYPE] * len(node.params))
        
        if self.symbol_table.lookup_local(node.name):
            self._error(f'Функция \"{node.name}\" уже объявлена', node)
        
        symbol = Symbol(node.name, func_type, 'function', 0, 0)
        self.symbol_table.insert(node.name, symbol)
        
        self.symbol_table.enter_scope()
        self.current_function_return_type = return_type
        
        for param_name in node.params:
            if self.symbol_table.lookup_local(param_name):
                self._error(f'Параметр \"{param_name}\" уже объявлен', node)
            symbol = Symbol(param_name, INT_TYPE, 'param', 0, 0)
            self.symbol_table.insert(param_name, symbol)
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        self.symbol_table.exit_scope()

    def visit_statement(self, node):
        if isinstance(node, VarDecl):
            self.visit_var_decl(node)
        elif isinstance(node, ReturnStmt):
            self.visit_return_stmt(node)
        elif isinstance(node, (BinaryExpr, LiteralExpr, IdentifierExpr)):
            self.visit_expression(node)

    def visit_var_decl(self, node: VarDecl):
        if self.symbol_table.lookup_local(node.name):
            self._error(f'Переменная \"{node.name}\" уже объявлена', node)
        
        value_type = self.visit_expression(node.value)
        symbol = Symbol(node.name, value_type, 'var', 0, 0)
        self.symbol_table.insert(node.name, symbol)

    def visit_return_stmt(self, node: ReturnStmt):
        return_type = self.visit_expression(node.value)
        if not is_compatible(return_type, self.current_function_return_type):
            self._error(
                f'Несовпадение типов в return функции \"{self.current_function_name}\": '
                f'ожидался {self.current_function_return_type}, получен {return_type}', 
                node
            )

    def visit_expression(self, node):
        if isinstance(node, LiteralExpr):
            return INT_TYPE if isinstance(node.value, int) else FLOAT_TYPE
        
        elif isinstance(node, IdentifierExpr):
            symbol = self.symbol_table.lookup(node.name)
            if not symbol:
                self._error(f'Необъявленная переменная \"{node.name}\"', node)
                return INT_TYPE
            return symbol.type
        
        elif isinstance(node, BinaryExpr):
            left_type = self.visit_expression(node.left)
            right_type = self.visit_expression(node.right)
            result_type = get_binary_result_type(left_type, node.operator, right_type)
            if result_type is None:
                self._error(f'Несовместимые типы для оператора \"{node.operator}\": {left_type} и {right_type}', node)
                return INT_TYPE
            return result_type
        
        return INT_TYPE

    def _error(self, message: str, node):
        self.errors.append(message)
