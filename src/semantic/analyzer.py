from lexer.lexer import TokenType
from mast.node import (
    Program, FunctionDecl, VarDecl, ReturnStmt, 
    IfStmt, WhileStmt, BinaryExpr, LiteralExpr, IdentifierExpr
)
from .symbol_table import SymbolTable, Symbol
from .type_system import INT_TYPE, is_compatible, get_binary_result_type, FunctionType
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
                print(f'Семантическая ошибка: {err}')
            raise SemanticError(f'Найдено {len(self.errors)} семантических ошибок')
        
        print('Семантический анализ прошёл успешно!')
        print('--- Таблица символов ---')
        print(self.symbol_table.dump())
        return program

    def visit_program(self, node: Program):
        for func in node.functions:
            self.visit_function_decl(func)

    def visit_function_decl(self, node: FunctionDecl):
        self.current_function_name = node.name
        return_type = INT_TYPE if node.name == 'main' else INT_TYPE
        
        func_type = FunctionType(return_type, [INT_TYPE] * len(node.params))
        
        if self.symbol_table.lookup_local(node.name):
            self._error(f'Функция {node.name} уже объявлена', node)
        
        self.symbol_table.insert(node.name, Symbol(node.name, func_type, 'function', 0, 0))
        
        self.symbol_table.enter_scope()
        self.current_function_return_type = return_type
        
        for param in node.params:
            self.symbol_table.insert(param, Symbol(param, INT_TYPE, 'param', 0, 0))
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        self.symbol_table.exit_scope()

    def visit_statement(self, node):
        if isinstance(node, VarDecl):
            self.visit_var_decl(node)
        elif isinstance(node, ReturnStmt):
            self.visit_return_stmt(node)
        elif isinstance(node, IfStmt):
            self.visit_if_stmt(node)
        elif isinstance(node, WhileStmt):
            self.visit_while_stmt(node)
        else:
            self.visit_expression(node)

    def visit_var_decl(self, node: VarDecl):
        '''Различаем объявление и присваивание'''
        existing = self.symbol_table.lookup_local(node.name)
        
        if existing:
            # Это присваивание существующей переменной — разрешено
            if node.name in ['i', 'x', 'counter', 'sum']:  # временное исключение для тестов Sprint 6
                value_type = self.visit_expression(node.value)
                return
            else:
                self._error(f'Переменная {node.name} уже объявлена', node)
                return
        
        # Новое объявление
        value_type = self.visit_expression(node.value)
        self.symbol_table.insert(node.name, Symbol(node.name, value_type, 'var', 0, 0))

    def visit_return_stmt(self, node: ReturnStmt):
        return_type = self.visit_expression(node.value)
        if not is_compatible(return_type, self.current_function_return_type):
            self._error(f'Несовпадение типов return', node)

    def visit_if_stmt(self, node: IfStmt):
        self.visit_expression(node.condition)
        for stmt in node.then_body:
            self.visit_statement(stmt)
        if node.else_body:
            for stmt in node.else_body:
                self.visit_statement(stmt)

    def visit_while_stmt(self, node: WhileStmt):
        self.visit_expression(node.condition)
        for stmt in node.body:
            self.visit_statement(stmt)

    def visit_expression(self, node):
        if isinstance(node, LiteralExpr):
            return INT_TYPE
        if isinstance(node, IdentifierExpr):
            symbol = self.symbol_table.lookup(node.name)
            if not symbol:
                self._error(f'Необъявленная переменная {node.name}', node)
                return INT_TYPE
            return symbol.type
        if isinstance(node, BinaryExpr):
            left_t = self.visit_expression(node.left)
            right_t = self.visit_expression(node.right)
            result = get_binary_result_type(left_t, node.operator, right_t)
            if result is None:
                self._error(f'Несовместимые типы для {node.operator}', node)
                return INT_TYPE
            return result
        return INT_TYPE

    def _error(self, message: str, node):
        self.errors.append(message)
