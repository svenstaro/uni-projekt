from .labelOperation import LabelOperation
from operands import Register, AluOperand2, LabelOperand


class AluOperation(LabelOperation):
    @staticmethod
    def buildAluOpcodes(opcodes):
        result = {}
        for (name, code) in opcodes.items():
            code = "0" + code
            result[name] = code + "0"
            result[name + "s"] = code + "1"
        return result

    opcodes = buildAluOpcodes.__func__({
        "add": "00000",
        "adc": "00001",
        "sub": "00100",
        "sbc": "00101",
        "rsb": "00110",
        "rsc": "00111",

        "mul": "10000",
        "mll": "10001",
        "div": "10010",

        "and": "01000",
        "orr": "01001",
        "xor": "01010",
        #"not"

        "lsl": "01100",
        "asr": "01101",
        "lsr": "01110",
        "rot": "01111"
    })

    def __init__(self, arg, position):
        LabelOperation.__init__(self, arg, position)
        op2 = LabelOperand.createLabelOperand(self.labels, self.position)
        op2.size = 17
        self.argTypes = [Register, Register, op2]