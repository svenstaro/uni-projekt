from .operation import Operation
from ..operands import Zero, Register, Opcodes


class StackOperation(Operation):
    opcodes = {"push": "1110000",
               "pop":  "1110100"}

    structure = [Opcodes(opcodes), Zero(21), Register]
