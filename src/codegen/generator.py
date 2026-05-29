from ir.ir import IRProgram, IRFunction, Assign, Binary, Return, Label, Jump, JumpIfZero, Call, Malloc, Store, Load, GetElementPtr
from .emitter import AssemblyEmitter

class CodeGenerator:
    def __init__(self):
        self.emitter = AssemblyEmitter()
        self.temp_counter = 0
        self.label_counter = 0

    def generate(self, ir_program: IRProgram) -> str:
        self.emitter.emit('section .text')
        self.emitter.emit('    global main')
        self.emitter.emit('    extern malloc')
        self.emitter.emit('    extern printf')
        self.emitter.emit('    extern free')
        self.emitter.emit('')

        for func in ir_program.functions:
            self._generate_function(func)

        self.emitter.emit('section .data')
        self.emitter.emit('    format db "%d", 10, 0')
        return self.emitter.get_code()

    def _new_temp(self) -> str:
        self.temp_counter += 1
        return f'tmp{self.temp_counter}'

    def _new_label(self) -> str:
        self.label_counter += 1
        return f'.L{self.label_counter}'

    def _generate_function(self, func: IRFunction):
        self.emitter.emit(f'{func.name}:')
        self.emitter.emit('    push rbp')
        self.emitter.emit('    mov rbp, rsp')
        self.emitter.emit('    sub rsp, 128')

        var_offset = {}
        next_offset = 8 

        def get_offset(var: str) -> int:
            if var not in var_offset:
                nonlocal next_offset
                var_offset[var] = next_offset
                next_offset += 8
            return var_offset[var]

        for instr in func.body:
            if isinstance(instr, Assign):
                off = get_offset(instr.dest)
                if isinstance(instr.value, int):
                    self.emitter.emit(f'    mov dword [rbp-{off}], {instr.value}')
                else:
                    src_off = get_offset(instr.value)
                    self.emitter.emit(f'    mov eax, dword [rbp-{src_off}]')
                    self.emitter.emit(f'    mov dword [rbp-{off}], eax')

            elif isinstance(instr, Binary):
                off = get_offset(instr.dest)
                left_off = get_offset(instr.left)
                right_off = get_offset(instr.right)
                self.emitter.emit(f'    mov eax, dword [rbp-{left_off}]')
                if instr.op == '+':
                    self.emitter.emit(f'    add eax, dword [rbp-{right_off}]')
                elif instr.op == '-':
                    self.emitter.emit(f'    sub eax, dword [rbp-{right_off}]')
                elif instr.op == '*':
                    self.emitter.emit(f'    imul eax, dword [rbp-{right_off}]')
                elif instr.op == '/':
                    self.emitter.emit(f'    xor edx, edx')
                    self.emitter.emit(f'    idiv dword [rbp-{right_off}]')
                self.emitter.emit(f'    mov dword [rbp-{off}], eax')

            elif isinstance(instr, Malloc):
                off = get_offset(instr.dest)
                size = int(instr.size) if instr.size.isdigit() else 0
                self.emitter.emit(f'    mov rdi, {size}')
                self.emitter.emit(f'    call malloc')
                self.emitter.emit(f'    mov [rbp-{off}], rax')

            elif isinstance(instr, Store):
                addr_off = get_offset(instr.address)
                value_off = get_offset(instr.value)
                self.emitter.emit(f'    mov rax, [rbp-{addr_off}]') 
                self.emitter.emit(f'    mov ecx, dword [rbp-{value_off}]')
                self.emitter.emit(f'    mov [rax], ecx')

            elif isinstance(instr, Load):
                dest_off = get_offset(instr.dest)
                addr_off = get_offset(instr.address)
                self.emitter.emit(f'    mov rax, [rbp-{addr_off}]')
                self.emitter.emit(f'    mov ecx, [rax]')
                self.emitter.emit(f'    mov dword [rbp-{dest_off}], ecx')

            elif isinstance(instr, GetElementPtr):
                dest_off = get_offset(instr.dest)
                base_off = get_offset(instr.base)
                index_off = get_offset(instr.index)
                self.emitter.emit(f'    mov rax, [rbp-{base_off}]')  
                self.emitter.emit(f'    mov rcx, [rbp-{index_off}]') 
                self.emitter.emit(f'    lea rax, [rax + rcx*4]')   
                self.emitter.emit(f'    mov [rbp-{dest_off}], rax')

            elif isinstance(instr, Call):
                if instr.name == 'printf':
                    fmt_off = get_offset(instr.args[0])
                    val_off = get_offset(instr.args[1])
                    self.emitter.emit(f'    mov rdi, [rbp-{fmt_off}]')
                    self.emitter.emit(f'    mov esi, dword [rbp-{val_off}]')
                    self.emitter.emit(f'    xor eax, eax')
                    self.emitter.emit(f'    call printf')
                else:
                    pass

            elif isinstance(instr, Return):
                if instr.value:
                    off = get_offset(instr.value)
                    self.emitter.emit(f'    mov eax, dword [rbp-{off}]')
                else:
                    self.emitter.emit(f'    mov eax, 0')
                self.emitter.emit('    jmp .return_label')

            elif isinstance(instr, Label):
                self.emitter.emit(f'{instr.name}:')

            elif isinstance(instr, Jump):
                self.emitter.emit(f'    jmp {instr.label}')

            elif isinstance(instr, JumpIfZero):
                cond_off = get_offset(instr.condition)
                self.emitter.emit(f'    cmp dword [rbp-{cond_off}], 0')
                self.emitter.emit(f'    je {instr.label}')

        self.emitter.emit('.return_label:')
        self.emitter.emit('    mov rsp, rbp')
        self.emitter.emit('    pop rbp')
        self.emitter.emit('    ret')
        self.emitter.emit('')