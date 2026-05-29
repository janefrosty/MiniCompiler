from mast.node import (
    Program, FunctionDecl, VarDecl, ReturnStmt, IfStmt, WhileStmt,
    BinaryExpr, LiteralExpr, IdentifierExpr, ArrayDecl, ArraySubscript
)
from .ir import (
    IRProgram, IRFunction, Assign, Binary, Return, Label, Jump, JumpIfZero,
    Malloc, Store, Load, GetElementPtr
)

class IRGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.array_ptrs = {}        # имя массива -> временная переменная (указатель)
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

    # ------------------------------------------------------------
    #  Обработка операторов (statement)
    # ------------------------------------------------------------
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
            # Присваивание (обычная переменная или элемент массива)
            self._generate_assignment(node, body)
        else:
            # Выражение как оператор (например, вызов функции)
            self._generate_expression(node, None, body)

    def _generate_var_decl(self, node: VarDecl, body: list):
        # Обычная переменная
        if isinstance(node.value, LiteralExpr):
            body.append(Assign(node.name, node.value.value))
        else:
            temp = self.new_temp()
            self._generate_expression(node.value, temp, body)
            body.append(Assign(node.name, temp))

    def _generate_array_decl(self, node: ArrayDecl, body: list):
        # Вычисляем общий размер массива в байтах
        # Для простоты считаем, что все размеры – целые литералы
        total_elements = 1
        for dim in node.dimensions:
            if isinstance(dim, LiteralExpr):
                total_elements *= dim.value
            else:
                # Если размер – выражение, его нужно вычислить во время выполнения
                # Здесь упрощаем: генерируем временную переменную и умножаем
                # Но по заданию спринта размеры должны быть константами
                dim_temp = self.new_temp()
                self._generate_expression(dim, dim_temp, body)
                # Здесь должно быть умножение, но оставим для простоты, предполагая константу
                # На практике нужно генерировать код для вычисления произведения
                pass
        size_bytes = total_elements * 4   # int = 4 байта
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

        # then
        for stmt in node.then_body:
            self._generate_statement(stmt, body)
        body.append(Jump(end_label))
        body.append(Label(else_label))

        # else
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

    # ------------------------------------------------------------
    #  Присваивание (левая часть может быть переменной или элементом массива)
    # ------------------------------------------------------------
    def _generate_assignment(self, node: BinaryExpr, body: list):
        # node.left – lvalue (IdentifierExpr или ArraySubscript)
        # node.right – rvalue
        if isinstance(node.left, IdentifierExpr):
            # Обычная переменная
            temp = self.new_temp()
            self._generate_expression(node.right, temp, body)
            body.append(Assign(node.left.name, temp))
        elif isinstance(node.left, ArraySubscript):
            # Присваивание элементу массива: arr[index] = expr
            # 1. Получить адрес элемента через GEP
            addr = self.new_temp()
            self._generate_gep(node.left, addr, body)
            # 2. Вычислить значение правой части
            val = self.new_temp()
            self._generate_expression(node.right, val, body)
            # 3. Store
            body.append(Store(addr, val))
        else:
            raise Exception(f"Invalid lvalue in assignment: {type(node.left)}")

    # ------------------------------------------------------------
    #  Вычисление GEP (GetElementPtr) для ArraySubscript
    # ------------------------------------------------------------
    def _generate_gep(self, subscript: ArraySubscript, dest: str, body: list):
        # subscript.array – это IdentifierExpr (имя массива)
        # subscript.indices – список индексов (поддерживаем только один индекс для простоты)
        if len(subscript.indices) != 1:
            raise Exception("Multidimensional arrays not yet supported")
        base_ptr = self.array_ptrs.get(subscript.array.name)
        if base_ptr is None:
            raise Exception(f"Array {subscript.array.name} not declared")
        # Вычисляем индекс
        idx_temp = self.new_temp()
        self._generate_expression(subscript.indices[0], idx_temp, body)
        # GEP: dest = base_ptr + idx * 4
        body.append(GetElementPtr(dest, base_ptr, idx_temp))

    # ------------------------------------------------------------
    #  Генерация выражений (рекурсивный обход AST)
    # ------------------------------------------------------------
    def _generate_expression(self, node, dest: str, body: list):
        """
        Генерирует код для выражения и сохраняет результат в 'dest'.
        Если dest == None, выражение используется как оператор (например, вызов функции)
        """
        if isinstance(node, LiteralExpr):
            if dest is not None:
                body.append(Assign(dest, node.value))
        elif isinstance(node, IdentifierExpr):
            if dest is not None:
                body.append(Assign(dest, node.name))
        elif isinstance(node, ArraySubscript):
            # Чтение элемента массива: нужно получить адрес и загрузить
            addr = self.new_temp()
            self._generate_gep(node, addr, body)
            if dest is not None:
                body.append(Load(dest, addr))
        elif isinstance(node, BinaryExpr):
            if node.operator == '=':
                # Присваивание внутри выражения (например, a = b = c)
                # Для простоты не поддерживаем, но можно реализовать
                self._generate_assignment(node, body)
                if dest is not None:
                    # Возвращаем значение правой части
                    temp = self.new_temp()
                    self._generate_expression(node.right, temp, body)
                    body.append(Assign(dest, temp))
            else:
                # Бинарная операция (+, -, *, /, ==, <, ...)
                left = self.new_temp()
                right = self.new_temp()
                self._generate_expression(node.left, left, body)
                self._generate_expression(node.right, right, body)
                if dest is not None:
                    body.append(Binary(dest, left, node.operator, right))
                else:
                    # Выражение как оператор – игнорируем результат
                    pass
        elif isinstance(node, CallExpr):
            # Вызов функции – пока упрощённо
            # Сохраняем результат, если dest указан
            for arg in node.args:
                temp = self.new_temp()
                self._generate_expression(arg, temp, body)
            if dest is not None:
                body.append(Assign(dest, 0))  # заглушка
        else:
            raise Exception(f"Unsupported expression type: {type(node)}")