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

    def run(self, entrypoint=0):
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
        if command == 0x43fffffc:
            return False
        self.pc += 4
        self.execute(command)
        return True

    def execute(self, command):
        if command & 0xC0000000 == 0x00000000:
            self.executeAluOp(command)
        elif command & 0xC0000000 == 0x40000000:
            self.executeJumpOp(command)
        elif command & 0xC0000000 == 0x80000000:
            self.executeMemOp(command)
        elif command & 0xE0000000 == 0xC0000000:
            self.executeAdrOp(command)
        elif command & 0xF0000000 == 0xE0000000:
            self.executeStackOperation(command)
        elif command & 0xFC000000 == 0xF0000000:
            self.executeCallOp(command)
        elif command & 0xFC000000 == 0xF8000000:
            self.executeSwiOp(command)
        elif command & 0xFC000000 == 0xFC000000:
            self.executeClkOp(command)
        else:
            print "INVALID OPCODE!"
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
            try:
                assert address & high != 0 and address >= 0
            except AssertionError as e:
                print self.pc, self.counter, address
                raise e
            address &= ~high
            self.mem[address:address+4] = int32to8(self.register[rdest])
        elif rdest != 0:
            if address & high == 0:
                self.register[rdest] = fetchFromRom(self.rom, address)
            else:
                assert address >= 0
                address &= ~high
                self.register[rdest] = int8to32(self.mem[address:address+4])

    def executeJumpOp(self, command):
        condition = (command & 0x3E000000) >> 25
        if conditionIsMet(self.flags, condition):
            self.doJump(command)

    def doJump(self, command):
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
                value -= 2 ** 32
            os.write(1, str(value)+'\n')

    def executeClkOp(self, command):
        op2 = command & 0x01FFFFFF
        _, src = op2decode(op2, 25)
        self.register[src] = self.counter

    def executeCallOp(self, command):
        self.register[15] = self.pc & mask
        self.doJump(command)

    def executeAdrOp(self, command):
        rdest = (command >> 25) & 0xF
        immsrc = command & 0xFFFFFF
        value = self.pc + immediatedecode(immsrc, 24)
        self.register[rdest] = value & mask

    def executeStackOperation(self, command):
        push = command & 0x08000000 == 0
        if push:
            op2 = command & 0x01FFFFFF
            r, src = op2decode(op2, 25)
            if r == 1:
                src = self.register[src]
            self.register[14] -= 4
            address = self.register[14]
            try:
                assert address & high and not address < 0
            except AssertionError as e:
                print self.pc, self.counter, address
                raise e
            finally:
                address &= ~high
                self.mem[address:address+4] = int32to8(src)
        else:
            rdest = command & 0xF
            address = self.register[14]
            try:
                assert address & high and not address < 0
            except AssertionError as e:
                print self.pc, address
                raise e
            finally:
                address &= ~high
                self.register[rdest] = int8to32(self.mem[address:address+4])
                self.register[14] += 4


class Flags:
    Z = 0
    N = 1
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
        return 1, op2 & 0xF
    else:
        value = immediatedecode(op2 & (op2mask - 1), size - 1)
        if relative:
            value += relative
        return 0, value & mask

@purefunction
def conditionIsMet(flags, condition):
    return (condition & 0x1) ^((condition & 0x10 and flags[Flags.Z]) \
                             | (condition & 0x08 and flags[Flags.N]) \
                             | (condition & 0x04 and flags[Flags.C]) \
                             | (condition & 0x02 and flags[Flags.O]))

def getParamsAlu(command):
    statusFlag = command & 0x20000000 != 0
    opcode = (command & 0x01E00000) >> 21
    rdest = (command & 0x1E000000) >> 25
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
        result = src1 & ~src2

    elif opcode == 0x8:
        result = src1 & src2
    elif opcode == 0x9:
        result = src1 | src2
    elif opcode == 0xA:
        result = src1 ^ src2
    elif opcode == 0xB:
        result = src1 | ~src2
    elif opcode == 0xC:
	assert 0 <= src2 < 32
        result = src1 << src2
    elif opcode == 0xD:
	assert 0 <= src2 < 32
        msb = src1 >> 31
        bitmask = ~((-msb) << src2) << (32-src2) if msb else 0
        result = (src1 >> src2) | bitmask
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

    flags = [zero, negative, carry, overflow]

    return flags, result & mask

@purefunction
def fetchFromRom(rom, address):
    return int8to32(rom[address:address+4])

@purefunction
def fetchInstruction(rom, address):
    assert not address < 0
    assert address & high != high
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
