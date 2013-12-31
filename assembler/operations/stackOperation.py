from .operation import Operation
from operands import Zero, Register, Opcodes, Operand2


class PopOperation(Operation):
    opcodes = {"pop":  "1110100"}

    structure = [Opcodes(opcodes), Zero(21), Register]

class PushOperation(Operation):
    opcodes = {"push" : "1110000"}

    structure = [Opcodes(opcodes), Operand2(25)]
