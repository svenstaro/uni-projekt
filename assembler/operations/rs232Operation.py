from .operation import Operation
from ..operands import Opcodes, Zero, Register, Operand2


class Rs232rx(Operation):
    opcodes = {"rsr": "1111110"}

    structure = [Opcodes(opcodes), Zero(21), Register]


class Rs232tx(Operation):
    opcodes = {"rst": "1111111"}

    structure = [Opcodes(opcodes), Operand2(25)]
