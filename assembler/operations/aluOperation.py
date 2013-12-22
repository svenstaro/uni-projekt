from .operation import Operation
from operands import Register, AluOperand2


class AluOperation(Operation):
    @staticmethod
    def buildAluOpcodes(opcodes):
        result = {}
        for (name, code) in opcodes.items():
            code = "00" + code
            result[name] = code + "0"
            result[name + "s"] = code + "1"
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
        #"not": "1011"

        "lsl": "1100",
        "asr": "1101",
        "lsr": "1110",
        "ror": "1111"
    })

    argTypes = [Register, Register, AluOperand2]
