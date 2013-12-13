import os

try:
    from rpython.rlib.jit import JitDriver, purefunction
except ImportError:
    class JitDriver(object):
        def __init__(self, **kw):
            pass

        def jit_merge_point(self, **kw):
            pass

        def can_enter_jit(self, **kw):
            pass

    def purefunction(f):
        return f


def get_location(pc):
    return "%s" % pc


class Cpu(object):
    mem = None
    register = [0]*16
    flags = [False]*4
    pc = 0
    counter = 0

    mask = 0xFFFFFFFF
    jitdriver = JitDriver(greens=['pc'],
                          reds='auto',
                          get_printable_location=get_location)

    def __init__(self, memorysize):
        self.mem = [0] * memorysize

    def fillMemory(self, contents):
        if isinstance(contents, type("")):
            contents = [ord(char) for char in contents]

        self.mem[0:len(contents)] = contents

    def run(self, entrypoint=0):
        self.pc = entrypoint
        while True:
            self.jitdriver.jit_merge_point(pc=self.pc)
            self.counter += 1
            command = self.fetch()
            if command == 0xe1000000:
                break
            self.execute(command)
            self.pc += 4

    def fetch(self):
        pc = self.pc
        assert not pc < 0
        return self.int8to32(self.mem[pc:pc+4])

    def execute(self, command):
        if command & 0xC0000000 == 0x00000000:
            self.executeAluOp(command)
        elif command & 0xC0000000 == 0x80000000:
            self.executeMemOp(command)
        elif command & 0xE0000000 == 0xC0000000:
            self.executeConditionalJumpOp(command)
        elif command & 0xFE000000 == 0xE0000000:
            self.executeJumpOp(command)
        elif command & 0xFE000000 == 0xE2000000:
            self.executeCallOp(command)
        elif command & 0xFE000000 == 0xE4000000:
            self.executeSwiOp(command)
        elif command & 0xE0000000 == 0x40000000:
            self.executeAdrOp(command)
        else:
            pass  # TODO: Invalid opcode

    @staticmethod
    @purefunction
    def executeAluOperation(opcode, src1, src2, c):
        result = 0
        if opcode == 0x0:
            result = src1 + src2
        elif opcode == 0x1:
            result = src1 + src2 + c
        elif opcode == 0x4:
            result = src1 - src2
        elif opcode == 0x5:
            result = src1 - src2 - c
        elif opcode == 0x6:
            result = src2 - src1
        elif opcode == 0x7:
            result = src2 - src1 - c

        elif opcode == 0x2:
            result = src1 * src2
        elif opcode == 0x3:
            result = src1 / src2

        elif opcode == 0x8:
            result = src1 & src2
        elif opcode == 0x9:
            result = src1 | src2
        elif opcode == 0xA:
            result = src1 ^ src2
        elif opcode == 0xB:
            result = ~src2

        elif opcode == 0xC:
            result = src1 << src2
        elif opcode == 0xD:
            result = src1 >> src2
        elif opcode == 0xE:
            result = src1 >> src2  # TODO LSR
        elif opcode == 0xF:
            pass  # TODO ROR

        negative = result < 0
        zero = result == 0
        carry = src1 < result and src2 < result
        overflow = src1 > result > src2

        flags = [negative, zero, carry, overflow]

        return flags, result & Cpu.mask

    @purefunction
    def getParamsAlu(self, command):
        statusFlag = command & 0x02000000 != 0
        opcode = (command & 0x3C000000) >> 26
        rdest = (command & 0x01E00000) >> 21
        rsrc1 = (command & 0x001E0000) >> 17
        aluop2 = (command & 0x0001FFFF)
        src1 = self.register[rsrc1]
        src2 = self.op2decode(aluop2, 17)  # TODO sign extension
        return opcode, rdest, src1, src2, statusFlag

    def executeAluOp(self, command):
        opcode, rdest, src1, src2, statusFlag = self.getParamsAlu(command)

        flags, result = Cpu.executeAluOperation(opcode, src1, src2, self.flags[Flags.C])

        if statusFlag:
            self.flags = flags

        if rdest != 0:
            self.register[rdest] = result

    @staticmethod
    @purefunction
    def immediatedecode(value, size):
        if value & (1 << (size - 1)) != 0:
            signmask = (1 << (32 - size)) - 1
            signmask <<= size
            value |= signmask
        return value & Cpu.mask

    @purefunction
    def op2decode(self, op2, size, relative=False):
        mask = 1 << (size - 1)
        if op2 & mask == 0:
            return self.register[(op2 >> (size - 1 - 4)) & 0xF]
        else:
            value = self.immediatedecode(op2 & (mask - 1), size - 1)
            if relative:
                value += self.pc
            return value & self.mask

    @purefunction
    def getParamsMem(self, command):
        store = command & 0x20000000 != 0
        relative = True  # command & 0x40000000 != 0
        rdest = (command & 0x1E000000) >> 25
        op2 = command & 0x01FFFFFF
        address = self.op2decode(op2, 25, relative)
        return address, rdest, store

    def executeMemOp(self, command):
        address, rdest, store = self.getParamsMem(command)
        if store:
            self.mem[address:address+4] = self.int32to8(self.register[rdest])
        elif rdest != 0:
            self.register[rdest] = self.int8to32(self.mem[address:address+4])

    @staticmethod
    @purefunction
    def int32to8(number):
        return [(number >> 24) & 0xFF,
                (number >> 16) & 0xFF,
                (number >> 8) & 0xFF,
                number & 0xFF]

    @staticmethod
    @purefunction
    def int8to32(array):
        number = 0
        for i in range(4):
            number <<= 8
            number |= array[i] if array[i] >= 0 else 0xff - ~array[i]
        return number & Cpu.mask

    def executeConditionalJumpOp(self, command):
        condition = (command & 0x1E000000) >> 25
        if self.conditionIsMet(self.flags, condition):
            self.executeJumpOp(command)

    @staticmethod
    @purefunction
    def conditionIsMet(flags, condition):
        if condition & 0xE == 0:
            return (condition & 0x1) ^ flags[Flags.Z]
        elif condition & 0xE == 0x8:
            return (condition & 1) ^ flags[Flags.O]
        elif condition & 0xE == 0x9:
            return (condition & 1) ^ flags[Flags.C]
        elif condition & 0xC == 0x4:  # lt, gt, ...
            return ((condition & 1) and flags[Flags.Z])\
                or ((condition & 0x2) >> 1) ^ flags[Flags.N]
        else:
            return False  # TODO: Invalid condition

    @purefunction
    def getParamsJump(self, command):
        op2 = command & 0x01FFFFFF
        src = self.op2decode(op2, 25, True)
        return src

    def executeJumpOp(self, command):
        self.pc -= 4
        src = self.getParamsJump(command)
        self.pc = src

    def executeSwiOp(self, command):
        op2 = command & 0x01FFFFFF
        src = self.op2decode(op2, 25)
        if src == 0:
            os.write(1, chr(self.register[1]))

    def executeCallOp(self, command):
        self.register[15] = self.pc & self.mask
        self.executeJumpOp(command)

    def executeAdrOp(self, command):
        rdest = (command >> 25) & 0xF
        immsrc = command & 0xFFFFFF
        value = self.pc + self.immediatedecode(immsrc, 24)
        self.register[rdest] = value & self.mask


class Flags:
    N = 0
    Z = 1
    C = 2
    O = 3
