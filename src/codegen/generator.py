from ir.ir import IRProgram, IRFunction, Assign, Binary, Return, Label, Jump, JumpIfZero, Call
from .emitter import AssemblyEmitter

class CodeGenerator:
    def __init__(self):
        self.emitter = AssemblyEmitter()

    def generate(self, ir_program: IRProgram) -> str:
        self.emitter.emit('section .text')
        self.emitter.emit('    global main')
        self.emitter.emit('    extern printf')
        self.emitter.emit('')

        for func in ir_program.functions:
            self._generate_function(func)

        self.emitter.emit('section .data')
        self.emitter.emit('    format db "%d", 10, 0')
        return self.emitter.get_code()

    def _generate_function(self, func):
        self.emitter.emit(f'{func.name}:')
        self.emitter.emit('    push rbp')
        self.emitter.emit('    mov rbp, rsp')
        self.emitter.emit('    sub rsp, 128')

        for instr in func.body:
            if isinstance(instr, Assign):
                self.emitter.emit(f'    mov dword [rbp-8], {instr.value if isinstance(instr.value, int) else "eax"}')
            elif isinstance(instr, Binary):
                self.emitter.emit(f'    mov eax, {instr.left}')
                self.emitter.emit(f'    add eax, {instr.right}')
                self.emitter.emit('    mov [rbp-16], eax')
            elif isinstance(instr, Call):
                self.emitter.emit('    mov rdi, format')
                self.emitter.emit('    xor rax, rax')
                self.emitter.emit('    call printf')
            elif isinstance(instr, Return):
                self.emitter.emit('    mov eax, 0')
                self.emitter.emit('    jmp .return_label')

        self.emitter.emit('    mov rsp, rbp')
        self.emitter.emit('    pop rbp')
        self.emitter.emit('    ret')
        self.emitter.emit('')
