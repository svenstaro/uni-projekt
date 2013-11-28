# vim: softtabstop=4:expandtab

from operation import Operation
from operands import Register,Operand2
from errors import EncodingError
import re


class AluOperation(Operation):
    def __init__(self, arg):
        super(AluOperation, self).__init__(arg, 4)
        self.opcodes = {
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
    #       "not": "01011",

            "lsl": "01100",
            "asr": "01101",
            "lsr": "01110",
            "rot": "01111"
        }


    def encodable(self):
        return self.opcodes.has_key(self.arg[0:3])

    def extractStatusflag(self,command):
        statusflag = "0"
        if command.endswith("s") and self.opcodes.has_key(command[:-1]):
            statusflag = "1"
            command = command[:-1]
        return (statusflag, command)

    def encode(self):
        try:
            (command, args) = AluOperation.splitLine(self.arg)
            (statusflag, command) = self.extractStatusflag(command)

            return "0" + self.opcodes[command] + statusflag + Register(args[0]).encode() + Register(
                args[1]).encode() + Operand2(args[2]).encode()
        except Exception,e:
            raise EncodingError(self.arg, "not a valid alu op.",e)

    def decodable(self):
        return re.match("^0[01]{31}$", self.arg)

    def decode(self):
        if not AluOperation.decodable(self.arg):
            raise EncodingError()

        line = self.arg

        opcode = (key for key,vals in self.opcodes.items() if vals == line[1:6]).next()
        statusflag = "" if line[6:7] ==0 else "s"
        regDest = Register.decode(line[7:11])
        regSrc1 = Register.decode(line[11:15])
        op2 = Operand2.decode(line[15:32])
        return opcode + statusflag + " " + regDest + ", " + regSrc1 + ", " + op2