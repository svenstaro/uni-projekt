from .operation import Operation
from operands import Register, AluOperand2, Const, Opcodes


class AluOperation(Operation):
    opcodes = {
        "add": "0000",
        "adc": "0001",
        "sub": "0100",
        "sbc": "0101",
        "rsb": "0110",
        "rsc": "0111",

        "mul": "0010",
        "andn":"0011",

        "and": "1000",
        "orr": "1001",
        "xor": "1010",
        "orn": "1011",

        "lsl": "1100",
        "asr": "1101",
        "lsr": "1110",
        "ror": "1111"
    }

    structure = [Const("00"), Const("0"), Register, Opcodes(opcodes), Register, AluOperand2]


class AluSOperation(AluOperation):
    opcodes = dict((cmd+"s", opcode) for (cmd,opcode) in AluOperation.opcodes.items())
    structure = [Const("00"), Const("1"), Register, Opcodes(opcodes), Register, AluOperand2]

