from operation import Operation
from operands import Register,Operand2
from errors import EncodingError


class AluOperation(Operation):
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
    argTypes = [Register, Register, Operand2]


    def getOperationName(self):
        #TODO: Extract find
        opcode = (key for key, vals in self.opcodes.items() if vals == self.arg[1:6]).next()
        statusflag = "" if self.arg[6:7] == 0 else "s"
        return opcode + statusflag

    def getOperands(self):
        regDest = Register.decode(self.arg[7:11])
        regSrc1 = Register.decode(self.arg[11:15])
        op2 = Operand2.decode(self.arg[15:32])
        return [regDest, regSrc1, op2]
