from mast.node import Program, FunctionDecl, VarDecl, ReturnStmt, BinaryExpr, LiteralExpr, IdentifierExpr
from .ir import IRProgram, IRFunction, Assign, Binary, Return, Label

class IRGenerator:
    def __init__(self):
        self.temp_counter = 0

    def new_temp(self) -> str:
        self.temp_counter += 1
        return f't{self.temp_counter}'

    def generate(self, program: Program) -> IRProgram:
        functions = []
        for func in program.functions:
            functions.append(self._generate_function(func))
        return IRProgram(functions)

    def _generate_function(self, node: FunctionDecl) -> IRFunction:
        body = []
        for stmt in node.body:
            self._generate_statement(stmt, body)
        return IRFunction(node.name, node.params, body)

    def _generate_statement(self, node, body: list):
        if isinstance(node, VarDecl):
            if isinstance(node.value, LiteralExpr):
                body.append(Assign(node.name, node.value.value))
            elif isinstance(node.value, BinaryExpr):
                temp = self.new_temp()
                self._generate_binary(node.value, temp, body)
                body.append(Assign(node.name, temp))
            else:
                body.append(Assign(node.name, node.value)) 
        elif isinstance(node, ReturnStmt):
            if isinstance(node.value, LiteralExpr):
                body.append(Return(node.value.value))
            elif isinstance(node.value, IdentifierExpr):
                body.append(Return(node.value.name))
            else:
                temp = self.new_temp()
                self._generate_expression(node.value, temp, body)
                body.append(Return(temp))

    def _generate_binary(self, node: BinaryExpr, dest: str, body: list):
        left = node.left
        right = node.right

        if isinstance(left, LiteralExpr):
            left_val = left.value
        elif isinstance(left, IdentifierExpr):
            left_val = left.name
        else:
            left_val = self.new_temp()
            self._generate_expression(left, left_val, body)

        if isinstance(right, LiteralExpr):
            right_val = right.value
        elif isinstance(right, IdentifierExpr):
            right_val = right.name
        else:
            right_val = self.new_temp()
            self._generate_expression(right, right_val, body)

        body.append(Binary(dest, left_val, node.operator, right_val))

    def _generate_expression(self, node, dest: str, body: list):
        if isinstance(node, BinaryExpr):
            self._generate_binary(node, dest, body)
