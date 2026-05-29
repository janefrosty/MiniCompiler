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
class Malloc(IRInstruction):
    dest: str 
    size: str 

@dataclass
class Store(IRInstruction):
    address: str  
    value: str  

@dataclass
class Load(IRInstruction):
    dest: str
    address: str

@dataclass
class GetElementPtr(IRInstruction):
    dest: str
    base: str 
    index: str  

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
                elif isinstance(instr, Malloc):
                    lines.append(f'  {instr.dest} = malloc({instr.size})')
                elif isinstance(instr, Store):
                    lines.append(f'  store {instr.value} -> [{instr.address}]')
                elif isinstance(instr, Load):
                    lines.append(f'  {instr.dest} = load [{instr.address}]')
                elif isinstance(instr, GetElementPtr):
                    lines.append(f'  {instr.dest} = gep {instr.base}[{instr.index}]')
            lines.append('')
        return '\n'.join(lines)