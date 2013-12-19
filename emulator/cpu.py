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
    return "pc=%s" % hex(pc)


class Cpu(object):
    mem = None
    rom = None
    register = [0]*16
    flags = [False]*4
    pc = 0
    counter = 0

    jitdriver = JitDriver(greens=['pc'],
                          reds='auto',
                          get_printable_location=get_location)

    def __init__(self, memorysize, rom):
        self.mem = [0] * memorysize
        self.fillRom(rom)

    def fillRom(self, contents):
        if isinstance(contents, type("")):
            contents = [ord(char) for char in contents]

        self.rom = contents + [0] * 4

    def run(self, entrypoint=0x80000000):
        self.pc = entrypoint
        try:
            while True:
                self.jitdriver.jit_merge_point(pc=self.pc)
                if not self.tick():
                    break
        except KeyboardInterrupt:
            print
            print "Aborted."

    def tick(self):
        self.counter += 1
        command = fetchInstruction(self.rom, self.pc)
        if command == 0xe1000000:
            return False
        self.execute(command)
        self.pc += 4
        return True

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
        elif command & 0xFE000000 == 0x64000000:
            self.executeSwiOp(command)
        elif command & 0xE0000000 == 0x40000000:
            self.executeAdrOp(command)
        elif command & 0x68000000 == 0x68000000:
            self.executeStackOperation(command)
        else:
            pass  # TODO: Invalid opcode

    def executeAluOp(self, command):
        opcode, statusFlag, rdest, rsrc1, op2 = getParamsAlu(command)
        r, src2 = op2decode(op2, 17)
        src1 = self.register[rsrc1]
        if r == 1:
            src2 = self.register[src2]

        flags, result = executeAluOperation(opcode, src1, src2, self.flags[Flags.C])

        if statusFlag:
            self.flags = flags

        if rdest != 0:
            self.register[rdest] = result

    def executeMemOp(self, command):
        store, rdest, op2 = getParamsMem(command)
        r, address = op2decode(op2, 25, self.pc)
        if r == 1:
            address = self.register[address]
        if store:
            assert address & high == 0
            assert address >= 0
            self.mem[address:address+4] = int32to8(self.register[rdest])
        elif rdest != 0:
            if address & high == high:
                self.register[rdest] = fetchFromRom(self.rom, address)
            else:
                assert address >= 0
                self.register[rdest] = int8to32(self.mem[address:address+4])

    def executeConditionalJumpOp(self, command):
        condition = (command & 0x1E000000) >> 25
        if conditionIsMet(self.flags, condition):
            self.executeJumpOp(command)

    def executeJumpOp(self, command):
        self.pc -= 4
        op2 = getParamsJump(command)
        r, dest = op2decode(op2, 25, self.pc)
        if r == 1:
            dest = self.register[dest]
        self.pc = dest

    def executeSwiOp(self, command):
        op2 = command & 0x01FFFFFF
        r, src = op2decode(op2, 25)
        if r == 1:
            src = self.register[src]
        if src == 0:
            os.write(1, chr(self.register[1]))
        elif src == 1:
            value = self.register[1]
            if value & high == high:
                value -= 2 **32
            os.write(1, str(value)+'\n')

    def executeCallOp(self, command):
        self.register[15] = self.pc & mask
        self.executeJumpOp(command)

    def executeAdrOp(self, command):
        rdest = (command >> 25) & 0xF
        immsrc = command & 0xFFFFFF
        value = self.pc + immediatedecode(immsrc, 24)
        self.register[rdest] = value & mask

    def executeStackOperation(self, command):
        push = command & 0x02000000 == 0
        rdest = command & 0xF
        if push:
            address = self.register[14]
            assert address >= 0
            self.mem[address:address+4] = int32to8(self.register[rdest])
            self.register[14] -= 4
        else:
            self.register[14] += 4
            address = self.register[14]
            assert address >= 0
            self.register[rdest] = int8to32(self.mem[address:address+4])


class Flags:
    N = 0
    Z = 1
    C = 2
    O = 3

mask = 0xFFFFFFFF
high = 0x80000000

@purefunction
def int32to8(number):
    return [(number >> 24) & 0xFF,
            (number >> 16) & 0xFF,
            (number >> 8) & 0xFF,
            number & 0xFF]

@purefunction
def int8to32(array):
    number = 0
    for i in range(4):
        number <<= 8
        number |= array[i] if array[i] >= 0 else 0xff - ~array[i]
    return number & mask

@purefunction
def immediatedecode(value, size):
    if value & (1 << (size - 1)) != 0:
        signmask = (1 << (32 - size)) - 1
        signmask <<= size
        value |= signmask
    return value & mask

@purefunction
def op2decode(op2, size, relative=0):
    op2mask = 1 << (size - 1)
    if op2 & op2mask == 0:
        return 1, (op2 >> (size - 1 - 4)) & 0xF
    else:
        value = immediatedecode(op2 & (op2mask - 1), size - 1)
        if relative:
            value += relative
        return 0, value & mask

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

def getParamsAlu(command):
    statusFlag = command & 0x02000000 != 0
    opcode = (command & 0x3C000000) >> 26
    rdest = (command & 0x01E00000) >> 21
    rsrc1 = (command & 0x001E0000) >> 17
    op2 = (command & 0x0001FFFF)
    return opcode, statusFlag, rdest, rsrc1, op2

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
        result = src2 - src1 + c

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
	assert 0 <= src2 < 32
        result = src1 << src2
    elif opcode == 0xD:
	assert 0 <= src2 < 32
        msb = src1 >> 31
        bitmask = ~((-msb) << src2) << (32-src2)
        result = (src1 >> src2) | mitmask
    elif opcode == 0xE:
        assert 0 <= src2 < 32
        result = src1 >> src2
    elif opcode == 0xF:
        assert 0 <= src2 < 32
        result = src1 >> src2 | src1 << (32-src2)

    negative = result & high != 0
    zero = result == 0
    carry = result & mask != result
    overflow = src1 & high == src2 & high and src1 & high != result & high

    flags = [negative, zero, carry, overflow]

    return flags, result & mask

@purefunction
def fetchFromRom(rom, address):
    address &= (high - 1)
    return int8to32(rom[address:address+4])

@purefunction
def fetchInstruction(rom, address):
    assert not address < 0
    assert address & high == high
    return fetchFromRom(rom, address)
    # return int8to32(self.mem[pc:pc+4])

@purefunction
def getParamsMem(command):
    store = command & 0x20000000 != 0
    rdest = (command & 0x1E000000) >> 25
    op2 = command & 0x01FFFFFF
    return store, rdest, op2

@purefunction
def getParamsJump(command):
    return command & 0x01FFFFFF
