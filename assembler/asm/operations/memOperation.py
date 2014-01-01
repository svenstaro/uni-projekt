from .operation import Operation
from ..operands import Register, LabelOperand, Opcodes


class MemOperation(Operation):
    opcodes = {"ld":  "100",
               "st":  "101",
               "adr": "110"}

    structure = [Opcodes(opcodes), Register, LabelOperand]
