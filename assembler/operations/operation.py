from structure import Structure


class Operation(Structure):
    def __init__(self, arg, size):
        super(Operation, self).__init__(arg)
        self.size = size

    @staticmethod
    def splitLine(line):
        (command, arguments) = line.split(" ", 1)
        args = [arg.strip() for arg in arguments.split(",")]
        return (command, args)

