from dataclasses import dataclass
from typing import List, Optional, Union

class IRInstruction: pass

@dataclass
class Label(IRInstruction):
    name: str

@dataclass
class Assign(IRInstruction):
    dest: str
    value: Union[int, str]

@dataclass
class Binary(IRInstruction):
    dest: str
    left: str
    op: str
    right: str

@dataclass
class Call(IRInstruction):
    dest: Optional[str]
    name: str
    args: List[str]

@dataclass
class Return(IRInstruction):
    value: Optional[str] = None

@dataclass
class Jump(IRInstruction):
    label: str

@dataclass
class JumpIfZero(IRInstruction):
    condition: str
    label: str

@dataclass
class IRFunction:
    name: str
    params: List[str]
    body: List[IRInstruction]

@dataclass
class IRProgram:
    functions: List[IRFunction]

    def dump(self) -> str:
        lines = []
        for func in self.functions:
            lines.append(f'function {func.name}():')
            for instr in func.body:
                if isinstance(instr, Label):
                    lines.append(f'  {instr.name}:')
                elif isinstance(instr, Assign):
                    lines.append(f'  {instr.dest} = {instr.value}')
                elif isinstance(instr, Binary):
                    lines.append(f'  {instr.dest} = {instr.left} {instr.op} {instr.right}')
                elif isinstance(instr, Call):
                    lines.append(f'  call {instr.name}({instr.args})')
                elif isinstance(instr, Return):
                    lines.append(f'  return {instr.value}')
                elif isinstance(instr, Jump):
                    lines.append(f'  jmp {instr.label}')
                elif isinstance(instr, JumpIfZero):
                    lines.append(f'  jz {instr.condition} -> {instr.label}')
            lines.append('')
        return '\n'.join(lines)
