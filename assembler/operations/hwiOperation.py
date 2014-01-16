from .operation import Operation
from ..operands import Register, Operand2, Opcodes, Zero


class LedOperation(Operation):

    opcodes = {"led": "1111100"}

    structure = [Opcodes(opcodes), Zero(21), Register]

class ButOperation(Operation):

    opcodes = {"but": "1111101"}

    structure = [Opcodes(opcodes), Operand2(25)]
