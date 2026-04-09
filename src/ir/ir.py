from dataclasses import dataclass
from typing import List, Optional, Union

class IRInstruction:
    pass

@dataclass
class Label(IRInstruction):
    name: str

@dataclass
class Assign(IRInstruction):
    dest: str
    value: Union[int, str, 'Binary']

@dataclass
class Binary(IRInstruction):
    dest: str
    left: str
    op: str
    right: str

@dataclass
class Return(IRInstruction):
    value: Optional[str] = None

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
            lines.append(f'function {func.name}({func.params}):')
            for instr in func.body:
                if isinstance(instr, Label):
                    lines.append(f'  {instr.name}:')
                elif isinstance(instr, Assign):
                    lines.append(f'  {instr.dest} = {instr.value}')
                elif isinstance(instr, Binary):
                    lines.append(f'  {instr.dest} = {instr.left} {instr.op} {instr.right}')
                elif isinstance(instr, Return):
                    lines.append(f'  return {instr.value if instr.value else ""}')
            lines.append('')
        return '\n'.join(lines)
