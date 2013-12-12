from .operation import Operation
from operands import Register, LabelOperand


class MemOperation(Operation):
    opcodes = {"ld":  "100",
               "st":  "101",
               "adr": "010"}

    argTypes = [Register, LabelOperand]
