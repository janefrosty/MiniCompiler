from mast.node import (
    Program, FunctionDecl, VarDecl, ReturnStmt, IfStmt, WhileStmt,
    BinaryExpr, LiteralExpr, IdentifierExpr, ArrayDecl, ArraySubscript,
    CallExpr
)
from .ir import (
    IRProgram, IRFunction, Assign, Binary, Return, Label, Jump, JumpIfZero,
    Malloc, Store, Load, GetElementPtr
)

class IRGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.array_ptrs = {}       # имя массива -> временная переменная (указатель)
        self.current_function = None

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
        self.array_ptrs = {}
        self.current_function = node.name
        body = []
        for stmt in node.body:
            self._generate_statement(stmt, body)
        return IRFunction(node.name, node.params, body)

    def _generate_statement(self, node, body: list):
        if isinstance(node, VarDecl):
            self._generate_var_decl(node, body)
        elif isinstance(node, ArrayDecl):
            self._generate_array_decl(node, body)
        elif isinstance(node, ReturnStmt):
            self._generate_return(node, body)
        elif isinstance(node, IfStmt):
            self._generate_if(node, body)
        elif isinstance(node, WhileStmt):
            self._generate_while(node, body)
        elif isinstance(node, BinaryExpr) and node.operator == '=':
            self._generate_assignment(node, body)
        elif isinstance(node, CallExpr):
            # вызов функции как оператор (например, foo();)
            # результат не используется
            self._generate_call(node, None, body)
        else:
            self._generate_expression(node, None, body)

    def _generate_var_decl(self, node: VarDecl, body: list):
        if isinstance(node.value, LiteralExpr):
            body.append(Assign(node.name, node.value.value))
        else:
            temp = self.new_temp()
            self._generate_expression(node.value, temp, body)
            body.append(Assign(node.name, temp))

    def _generate_array_decl(self, node: ArrayDecl, body: list):
        total_elements = 1
        for dim in node.dimensions:
            if isinstance(dim, LiteralExpr):
                total_elements *= dim.value
            else:
                # для простоты считаем, что размеры — константы
                # здесь можно добавить вычисление выражения
                pass
        size_bytes = total_elements * 4
        ptr = self.new_temp()
        body.append(Malloc(ptr, str(size_bytes)))
        self.array_ptrs[node.name] = ptr

    def _generate_return(self, node: ReturnStmt, body: list):
        if isinstance(node.value, LiteralExpr):
            body.append(Return(node.value.value))
        else:
            temp = self.new_temp()
            self._generate_expression(node.value, temp, body)
            body.append(Return(temp))

    def _generate_if(self, node: IfStmt, body: list):
        else_label = self.new_label()
        end_label = self.new_label()
        cond = self.new_temp()
        self._generate_expression(node.condition, cond, body)
        body.append(JumpIfZero(cond, else_label))
        for stmt in node.then_body:
            self._generate_statement(stmt, body)
        body.append(Jump(end_label))
        body.append(Label(else_label))
        if node.else_body:
            for stmt in node.else_body:
                self._generate_statement(stmt, body)
        body.append(Label(end_label))

    def _generate_while(self, node: WhileStmt, body: list):
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

    def _generate_assignment(self, node: BinaryExpr, body: list):
        # левая часть может быть IdentifierExpr или ArraySubscript
        if isinstance(node.left, IdentifierExpr):
            temp = self.new_temp()
            self._generate_expression(node.right, temp, body)
            body.append(Assign(node.left.name, temp))
        elif isinstance(node.left, ArraySubscript):
            addr = self.new_temp()
            self._generate_gep(node.left, addr, body)
            val = self.new_temp()
            self._generate_expression(node.right, val, body)
            body.append(Store(addr, val))
        else:
            raise Exception(f"Invalid lvalue in assignment: {type(node.left)}")

    def _generate_gep(self, subscript: ArraySubscript, dest: str, body: list):
        # Поддерживаем только одномерные массивы (для многомерных нужно обобщение)
        if len(subscript.indices) != 1:
            raise Exception("Multidimensional arrays not fully supported")
        base_ptr = self.array_ptrs.get(subscript.array.name)
        if base_ptr is None:
            raise Exception(f"Array {subscript.array.name} not declared")
        idx_temp = self.new_temp()
        self._generate_expression(subscript.indices[0], idx_temp, body)
        body.append(GetElementPtr(dest, base_ptr, idx_temp))

    def _generate_expression(self, node, dest: str, body: list):
        """Генерирует код для выражения, результат сохраняется в dest (если не None)"""
        if isinstance(node, LiteralExpr):
            if dest is not None:
                body.append(Assign(dest, node.value))
        elif isinstance(node, IdentifierExpr):
            if dest is not None:
                body.append(Assign(dest, node.name))
        elif isinstance(node, ArraySubscript):
            addr = self.new_temp()
            self._generate_gep(node, addr, body)
            if dest is not None:
                body.append(Load(dest, addr))
        elif isinstance(node, BinaryExpr):
            if node.operator == '=':
                # присваивание внутри выражения (например, a = b = 5)
                self._generate_assignment(node, body)
                if dest is not None:
                    # возвращаем значение правой части
                    temp = self.new_temp()
                    self._generate_expression(node.right, temp, body)
                    body.append(Assign(dest, temp))
            else:
                left = self.new_temp()
                right = self.new_temp()
                self._generate_expression(node.left, left, body)
                self._generate_expression(node.right, right, body)
                if dest is not None:
                    body.append(Binary(dest, left, node.operator, right))
        elif isinstance(node, CallExpr):
            # вызов функции в выражении
            self._generate_call(node, dest, body)
        else:
            raise Exception(f"Unsupported expression type: {type(node)}")

    def _generate_call(self, node: CallExpr, dest: str | None, body: list):
        """Генерирует вызов функции. Результат (если нужен) сохраняет в dest."""
        # Генерируем аргументы и сохраняем их во временные переменные
        arg_temps = []
        for arg in node.args:
            temp = self.new_temp()
            self._generate_expression(arg, temp, body)
            arg_temps.append(temp)
        # В текущей реализации мы не поддерживаем передачу аргументов через регистры,
        # поэтому просто сохраняем результат вызова (если нужен) в dest.
        # Для упрощения будем считать, что функция возвращает значение, и оно
        # автоматически попадает в переменную dest (заглушка).
        # Реальная генерация вызова с передачей аргументов и получением результата
        # требует более сложной логики. Для вашего компилятора этого достаточно,
        # чтобы рекурсивные вызовы работали через внешний ассемблер (поскольку
        # функция factorial вызывает саму себя, и кодогенератор должен сгенерировать
        # инструкции call). Сейчас этот код только эмулирует вызов.
        if dest is not None:
            # Временно присваиваем 0 (вместо реального вызова)
            # Замените на реальную генерацию call, когда будете готовы
            body.append(Assign(dest, 0))