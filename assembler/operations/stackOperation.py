from .operation import Operation
from operands import Ignore, Register


class StackOperation(Operation):
    class Ignore21(Ignore):
        size = 21
    opcodes = {"push": "0110100",
               "pop":  "0110101"}

    argTypes = [Ignore21, Register]