from operations import AluOperation
from operands import Register, AluOperand2


class TwoOpAluOperation(AluOperation):
    opcodes = AluOperation.buildAluOpcodes({"not": "01011",
                                            "mov": "00000"})
    argTypes = [Register, AluOperand2]

    # We have to skip the empty operand:

    def buildEncodedOperation(self, command, args):
        return self.opcodes[command] + args[0] + "0" * 4 + args[1]

    def decodeArguments(self, remainder):
        remainder = remainder[0:4] + remainder[8:25]
        return AluOperation.decodeArguments(self, remainder)

    def decodable(self):
        return AluOperation.decodable(self) and self.arg[4:8] == "0"*4