# vim: softtabstop=4:expandtab


class Operation(object):
    @staticmethod
    def splitLine(line):
        (command, arguments) = line.split(" ", 1)
        args = [arg.strip() for arg in arguments.split(",")]
        return (command, args)

