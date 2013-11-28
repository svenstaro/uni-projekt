from operation import Operation
from operands import Register, OtherOperand2


class MemOperation(Operation):
    opcodes = {"ld": "101",
               "str": "100"}
    argTypes = [Register, OtherOperand2]