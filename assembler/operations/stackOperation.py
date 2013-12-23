from .operation import Operation
from operands import Ignore, Register


class StackOperation(Operation):
    class Ignore21(Ignore):
        size = 21
    opcodes = {"push": "1110000",
               "pop":  "1110100"}

    argTypes = [Ignore21, Register]
