from .operation import Operation
from operands import LabelOperand


class JumpOperation(Operation):

    argTypes = [LabelOperand]

    opcodes = {"call": "1111000"}

    conditions = {
        "mp": "00001",
        # equal or zero
        "eq": "10000",
        "z":  "10000",
        "ne": "10001",
        "nz": "10001",
        # lower than
        "lt": "01000",
        "n":  "01000",
        "le": "11000",
        # greater than
        "gt": "11001",
        "nn": "11001",
        "ge": "01001",
        # overflow
        "o":  "00010",
        "no": "00011",
        # carry
        "c":  "00100",
        "nc": "00101"}

    for (name, code) in conditions.items():
        opcodes["j" + name] = "01" + code
