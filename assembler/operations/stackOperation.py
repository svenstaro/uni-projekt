from .operation import Operation
from operands import Zero, Register


class StackOperation(Operation):
    opcodes = {"push": "1110000",
               "pop":  "1110100"}

    argTypes = [Zero(21), Register]
