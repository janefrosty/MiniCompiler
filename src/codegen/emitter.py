class AssemblyEmitter:
    def __init__(self):
        self.lines = []
        self.label_counter = 0

    def emit(self, line: str):
        self.lines.append(line)

    def label(self, name: str):
        self.lines.append(f'{name}:')

    def get_code(self) -> str:
        return '\n'.join(self.lines)

    def new_label(self) -> str:
        self.label_counter += 1
        return f'.L{self.label_counter}'
