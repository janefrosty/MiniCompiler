from lexer.lexer import TokenType
from mast.node import Program, FunctionDecl, VarDecl, ReturnStmt, IfStmt, WhileStmt, CallExpr, BinaryExpr, LiteralExpr, IdentifierExpr
from .symbol_table import SymbolTable, Symbol
from .type_system import INT_TYPE, FunctionType
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
            raise SemanticError(f'Найдено {len(self.errors)} ошибок')
        print('Семантический анализ прошёл успешно!')
        print('--- Таблица символов ---')
        print(self.symbol_table.dump())
        return program

    def visit_program(self, node: Program):
        for func in node.functions:
            self.visit_function_decl(func)

    def visit_function_decl(self, node: FunctionDecl):
        self.current_function_name = node.name
        return_type = INT_TYPE
        func_type = FunctionType(return_type, [INT_TYPE] * len(node.params))
        
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
        elif isinstance(node, CallExpr):
            self.visit_call_expr(node)

    def visit_var_decl(self, node: VarDecl):
        if self.symbol_table.lookup_local(node.name):
            # Присваивание
            self.visit_expression(node.value)
            return
        value_type = self.visit_expression(node.value)
        self.symbol_table.insert(node.name, Symbol(node.name, value_type, 'var', 0, 0))

    def visit_return_stmt(self, node):
        self.visit_expression(node.value)

    def visit_if_stmt(self, node):
        self.visit_expression(node.condition)
        for s in node.then_body:
            self.visit_statement(s)
        if node.else_body:
            for s in node.else_body:
                self.visit_statement(s)

    def visit_while_stmt(self, node):
        self.visit_expression(node.condition)
        for s in node.body:
            self.visit_statement(s)

    def visit_call_expr(self, node: CallExpr):
        for arg in node.args:
            self.visit_expression(arg)

    def visit_expression(self, node):
        if isinstance(node, LiteralExpr):
            return INT_TYPE
        if isinstance(node, IdentifierExpr):
            if not self.symbol_table.lookup(node.name):
                self._error(f'Необъявленная переменная {node.name}', node)
            return INT_TYPE
        if isinstance(node, BinaryExpr):
            self.visit_expression(node.left)
            self.visit_expression(node.right)
            return INT_TYPE
        if isinstance(node, CallExpr):
            self.visit_call_expr(node)
            return INT_TYPE
        return INT_TYPE

    def _error(self, message: str, node):
        self.errors.append(message)
