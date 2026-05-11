from mast.node import Program, FunctionDecl, VarDecl, ReturnStmt, IfStmt, WhileStmt, BinaryExpr, LiteralExpr, IdentifierExpr
from .ir import IRProgram, IRFunction, Assign, Binary, Return, Label, Jump, JumpIfZero

class IRGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self) -> str:
        self.temp_counter += 1
        return f't{self.temp_counter}'

    def new_label(self) -> str:
        self.label_counter += 1
        return f'L{self.label_counter}'

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
            self._generate_var_decl(node, body)
        elif isinstance(node, ReturnStmt):
            self._generate_return(node, body)
        elif isinstance(node, IfStmt):
            self._generate_if(node, body)
        elif isinstance(node, WhileStmt):
            self._generate_while(node, body)

    def _generate_var_decl(self, node, body):
        if isinstance(node.value, LiteralExpr):
            body.append(Assign(node.name, node.value.value))
        else:
            temp = self.new_temp()
            self._generate_expression(node.value, temp, body)
            body.append(Assign(node.name, temp))

    def _generate_return(self, node, body):
        if isinstance(node.value, LiteralExpr):
            body.append(Return(node.value.value))
        else:
            temp = self.new_temp()
            self._generate_expression(node.value, temp, body)
            body.append(Return(temp))

    def _generate_if(self, node: IfStmt, body):
        else_label = self.new_label()
        end_label = self.new_label()

        # Вычисляем условие
        cond = self.new_temp()
        self._generate_expression(node.condition, cond, body)
        
        body.append(JumpIfZero(cond, else_label))
        
        # Then branch
        for stmt in node.then_body:
            self._generate_statement(stmt, body)
        
        body.append(Jump(end_label))
        body.append(Label(else_label))
        
        # Else branch
        if node.else_body:
            for stmt in node.else_body:
                self._generate_statement(stmt, body)
        
        body.append(Label(end_label))

    def _generate_while(self, node: WhileStmt, body):
        start_label = self.new_label()
        end_label = self.new_label()

        body.append(Label(start_label))
        
        cond = self.new_temp()
        self._generate_expression(node.condition, cond, body)
        body.append(JumpIfZero(cond, end_label))
        
        for stmt in node.body:
            self._generate_statement(stmt, body)
        
        body.append(Jump(start_label))
        body.append(Label(end_label))

    def _generate_expression(self, node, dest: str, body):
        if isinstance(node, LiteralExpr):
            body.append(Assign(dest, node.value))
        elif isinstance(node, IdentifierExpr):
            body.append(Assign(dest, node.name))
        elif isinstance(node, BinaryExpr):
            left = self.new_temp()
            right = self.new_temp()
            self._generate_expression(node.left, left, body)
            self._generate_expression(node.right, right, body)
            body.append(Binary(dest, left, node.operator, right))
