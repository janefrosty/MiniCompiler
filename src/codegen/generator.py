from ir.ir import IRProgram, IRFunction, Assign, Binary, Return, Label, Jump, JumpIfZero
from .emitter import AssemblyEmitter

class CodeGenerator:
    def __init__(self):
        self.emitter = AssemblyEmitter()
        self.var_offset = {}
        self.next_offset = -8

    def generate(self, ir_program: IRProgram) -> str:
        self.emitter.emit('section .text')
        self.emitter.emit('    global main')
        self.emitter.emit('')

        for func in ir_program.functions:
            self._generate_function(func)

        return self.emitter.get_code()

    def _generate_function(self, func: IRFunction):
        self.var_offset.clear()
        self.next_offset = -8

        self.emitter.emit(f'{func.name}:')
        self.emitter.emit('    push rbp')
        self.emitter.emit('    mov rbp, rsp')
        self.emitter.emit('    sub rsp, 128')

        for instr in func.body:
            if isinstance(instr, Label):
                self.emitter.emit(f'{instr.name}:')
            elif isinstance(instr, Assign):
                self._generate_assign(instr)
            elif isinstance(instr, Binary):
                self._generate_binary(instr)
            elif isinstance(instr, Jump):
                self.emitter.emit(f'    jmp {instr.label}')
            elif isinstance(instr, JumpIfZero):
                self.emitter.emit(f'    cmp {instr.condition}, 0')
                self.emitter.emit(f'    je {instr.label}')
            elif isinstance(instr, Return):
                self._generate_return(instr)

        self.emitter.emit('    mov rsp, rbp')
        self.emitter.emit('    pop rbp')
        self.emitter.emit('    ret')
        self.emitter.emit('')

    def _generate_assign(self, instr):
        if isinstance(instr.value, int):
            offset = self._get_offset(instr.dest)
            self.emitter.emit(f'    mov dword [rbp{offset}], {instr.value}    ; {instr.dest} = {instr.value}')
        else:
            offset = self._get_offset(instr.dest)
            self.emitter.emit(f'    mov dword [rbp{offset}], eax         ; {instr.dest}')

    def _generate_binary(self, instr):
        self.emitter.emit(f'    mov eax, {instr.left}')
        if instr.op == '+':
            self.emitter.emit(f'    add eax, {instr.right}')
        elif instr.op == '-':
            self.emitter.emit(f'    sub eax, {instr.right}')
        offset = self._get_offset(instr.dest)
        self.emitter.emit(f'    mov [rbp{offset}], eax')

    def _generate_return(self, instr):
        if instr.value is not None:
            self.emitter.emit(f'    mov eax, {instr.value}')
        self.emitter.emit('    jmp .return_label')

    def _get_offset(self, var_name):
        if var_name not in self.var_offset:
            self.var_offset[var_name] = self.next_offset
            self.next_offset -= 8
        return self.var_offset[var_name]
