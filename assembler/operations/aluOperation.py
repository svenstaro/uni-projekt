from .operation import Operation
from operands import Register, AluOperand2


class AluOperation(Operation):
    @staticmethod
    def buildAluOpcodes(opcodes):
        result = {}
        for (name, code) in opcodes.items():
            result[name] = "000" + code
            result[name + "s"] = "001" + code
        return result

    opcodes = buildAluOpcodes.__func__({
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
    })

    argTypes = [Register, Register, AluOperand2]
