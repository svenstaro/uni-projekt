# vim: softtabstop=4:expandtab

from operations.operation import Operation


class AluOperation(Operation):
    opcodes = {
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
        "not": "01011",

        "lsl": "01100",
        "asr": "01101",
        "lsr": "01110",
        "rot": "01111"
    }


    @staticmethod
    def isA(line):
        return AluOperation.opcodes.has_key(arg[0:3])

    @staticmethod
    def extractStatusflag(command):
        statusflag = "0"
        if command.endswith("s") and alu_ops.has_key(command[:-1]):
            statusflag = "1"
            command = command[:-1]
        return (statusflag, command)


    @staticmethod
    def encode(line):
        (command, args) = AluOperation.splitLine(line)
        (statusflag, command) = AluOperation.extractStatusflag(command)

        return "0" + AluOperation.opcodes[command] + statusflag + Register.encode(args[0]) + Register.encode(
            args[1]) + Operand2.encode(args[2])

    @staticmethod
    def decode(line):
        raise NotImplementedError()
