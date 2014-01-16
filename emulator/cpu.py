import os

# Use dummy functions if no jit available
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
    """
    Returns a humanreadable location (for jit debugging)
    """
    return "pc=%s" % hex(pc)


class InvalidCommandError(Exception):
    pass


class InvalidAddressError(Exception):
    pass


class WriteToRomError(InvalidAddressError):
    pass

class Cpu(object):
    _jitdriver = JitDriver(greens=['pc'],
                           reds='auto',
                           get_printable_location=get_location)

    mem = []  #: Memory cells
    rom = []  #: ROM cells
    register = []  #: Registers
    flags = []  #: Flag list
    pc = 0  #: Program counter. Points to the next instruction executed
    counter = 0  #: Number of executed instructions

    def __init__(self, memorysize, rom):
        """
        memorysize -- Size of memory in bytes
        rom -- Rom contents
        """
        self.memorysize = memorysize

        self.setRomContents(rom)
        self.reset()

    def reset(self):
        """
        Resets the cpu to initial state
        """
        self.mem = [0] * self.memorysize
        self.register = [0]*16
        self.flags = [False]*4
        self.pc = 0
        self.counter = 0

    def setRomContents(self, contents):
        """
        Sets the rom contents
        contents -- String or list of ints
        """
        if isinstance(contents, type("")):
            contents = [ord(char) for char in contents]

        self.rom = contents + [0] * 4

    def run(self):
        """
        Starts program execution. Runs till halt-command.
        """
        try:
            while True:
                self._jitdriver.jit_merge_point(pc=self.pc)
                if not self.tick():
                    break
        except KeyboardInterrupt:
            print
            print "Aborted."

    def tick(self):
        """
        Executes one instruction.
        """
        self.counter += 1
        command = self.fetchFromRom(self.rom, self.pc)
        if command == 0x43fffffc:
            return False
        self.pc += 4
        self.__execute(command)
        return True

    # steps one cpu clock forwards. In this step the next command 
    # after the given entrypoint will be executed. 
    # If a breakpoint is found or the eof is reached, False is returned.
    def stepFrom(self, entrypoint=0x0):
        self.pc = entrypoint
        self._jitdriver.jit_merge_point(pc=self.pc)
        if self.tick():
            return self.pc
        return False

    def getFlags(self):
        return self.flags

    def getRegister(self):
        return self.register
        
    def stopExecution(self):
        self.running = False

    def __execute(self, command):
        """
        Executes a command.
        """
        if command & 0xC0000000 == 0x00000000:
            self.__executeAluOp(command)
        elif command & 0xC0000000 == 0x40000000:
            self.__executeJumpOp(command)
        elif command & 0xC0000000 == 0x80000000:
            self.__executeMemOp(command)
        elif command & 0xE0000000 == 0xC0000000:
            self.__executeAdrOp(command)
        elif command & 0xF0000000 == 0xE0000000:
            self.__executeStackOp(command)
        elif command & 0xFC000000 == 0xF0000000:
            self.__executeCallOp(command)
        elif command & 0xFC000000 == 0xF4000000:
            self.__executeClkOp(command)
        elif command & 0xFEC00000 == 0xF8000000:
            self.__executeLedOp(command)
        elif command & 0xFEC00000 == 0xFA000000:
            self.__executeButOp(command)
        elif command & 0xFC000000 == 0xFC000000:
            self.__executeRs232Op(command)
        else:
            raise InvalidCommandError()

    def __executeAluOp(self, command):
        opcode, statusFlag, rdest, rsrc1, op2 = self.__getParamsAlu(command)
        r, src2 = self.__op2decode(op2, 17)
        src1 = self.register[rsrc1]
        if r == 1:
            src2 = self.register[src2]

        flags, result = self.__executeAluOperation(opcode, src1, src2, self.flags[self.Flags.C])

        if statusFlag:
            self.flags = flags

        if rdest != 0:
            self.register[rdest] = result

    def __executeMemOp(self, command):
        store, rdest, op2 = self.__getParamsMem(command)
        r, address = self.__op2decode(op2, 25, self.pc)
        if r == 1:
            address = self.register[address]
        if store:
            self.__store(address, self.register[rdest])
        elif rdest != 0:
            self.register[rdest] = self.load(address)

    def __executeJumpOp(self, command):
        condition = (command & 0x3E000000) >> 25
        if self.__conditionIsMet(self.flags, condition):
            self.__doJump(command)

    def __doJump(self, command):
        op2 = command & 0x01FFFFFF
        r, dest = self.__op2decode(op2, 25, self.pc)
        if r == 1:
            dest = self.register[dest]
        self.pc = dest

    def __executeClkOp(self, command):
        op2 = command & 0x01FFFFFF
        r, src = self.__op2decode(op2, 25)

        if not r:
            raise InvalidCommandError()

        self.register[src] = self.counter

    def __executeCallOp(self, command):
        self.register[15] = self.pc & self.__mask
        self.__doJump(command)

    def __executeLedOp(self, command):
        op2 = command & 0x01FFFFFF
        r, src= self.__op2decode(op2, 25)
        if r == 1:
            src = self.register[src]
        # TODO: Do something useful 
        
    def __executeButOp(self, command):
        dest = command & 0xF
        self.register[dest] = 0
        # TODO: Do something useful

    def __executeRs232Op(self, command):
        transmit = command & 0x02000000
        if transmit:
            op2 = command & 0x01FFFFFF
            r, dest = self.__op2decode(op2, 25)
            if r == 1:
                dest = self.register[dest]
            dest = dest & 0xFF
            os.write(1, chr(dest))
        else:
            raise NotImplementedError()

    def __executeAdrOp(self, command):
        rdest = (command >> 25) & 0xF
        immsrc = command & 0xFFFFFF
        value = self.pc + self.__immediatedecode(immsrc, 24)
        self.register[rdest] = value & self.__mask

    def __executeStackOp(self, command):
        push = command & 0x08000000 == 0
        if push:
            op2 = command & 0x01FFFFFF
            r, src = self.__op2decode(op2, 25)
            if r == 1:
                src = self.register[src]
            self.register[14] -= 4
            address = self.register[14]
            self.__store(address, src)
        else:
            rdest = command & 0xF
            address = self.register[14]
            self.register[rdest] = self.load(address)
            self.register[14] += 4

    class Flags:
        Z = 0
        N = 1
        C = 2
        O = 3

    __mask = 0xFFFFFFFF
    __high = 0x80000000

    def load(self, address):
        """
        Load the value from ram/rom at the specified address.
        The address should be 32bit aligned.
        """
        assert address >= 0
        try:
            if address & self.__high == 0:
                return self.fetchFromRom(self.rom, address)
            else:
                address &= ~self.__high
                return self.__int8to32(self.mem[address:address + 4])
        except IndexError:
            raise InvalidAddressError(address)

    def __store(self, address, value):
        assert address >= 0
        if address & self.__high == 0:
            raise WriteToRomError(address)

        address &= ~self.__high
        try:
            self.mem[address:address+4] = self.__int32to8(value)
        except IndexError:
            raise InvalidAddressError(address)

    @staticmethod
    @purefunction
    def __int32to8(number):
        """
        Converts a 32bit integer in big endian to an array of four 8bit integer.
        """
        return [(number >> 24) & 0xFF,
                (number >> 16) & 0xFF,
                (number >> 8) & 0xFF,
                number & 0xFF]

    @staticmethod
    @purefunction
    def __int8to32(array):
        """
        Converts an array of four 8bit integer to a 32bit integer in big endian.
        """
        number = 0
        for i in range(4):
            number <<= 8
            number |= array[i] if array[i] >= 0 else 0xff - ~array[i]
        return number & Cpu.__mask

    @staticmethod
    @purefunction
    def __immediatedecode(value, size):
        if value & (1 << (size - 1)) != 0:
            signmask = (1 << (32 - size)) - 1
            signmask <<= size
            value |= signmask
        return value & Cpu.__mask

    @staticmethod
    @purefunction
    def __op2decode(op2, size, relative=0):
        """
        Decodes an operand2. Returns the raw values (is_register, value)
        """
        op2mask = 1 << (size - 1)
        if op2 & op2mask == 0:
            return 1, op2 & 0xF
        else:
            value = Cpu.__immediatedecode(op2 & (op2mask - 1), size - 1)
            if relative:
                value += relative
            return 0, value & Cpu.__mask

    @staticmethod
    @purefunction
    def __conditionIsMet(flags, condition):
        """
        Checks whether a jump condition is true.
        """
        return (condition & 0x1) ^ ((condition & 0x10 and flags[Cpu.Flags.Z])
                                    | (condition & 0x08 and flags[Cpu.Flags.N])
                                    | (condition & 0x04 and flags[Cpu.Flags.C])
                                    | (condition & 0x02 and flags[Cpu.Flags.O]))

    @staticmethod
    @purefunction
    def __getParamsAlu(command):
        statusFlag = command & 0x20000000 != 0
        opcode = (command & 0x01E00000) >> 21
        rdest = (command & 0x1E000000) >> 25
        rsrc1 = (command & 0x001E0000) >> 17
        op2 = (command & 0x0001FFFF)
        return opcode, statusFlag, rdest, rsrc1, op2

    @staticmethod
    @purefunction
    def __executeAluOperation(opcode, src1, src2, c):
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
            if not 0 <= src2 < 32:
                raise InvalidCommandError()
            result = src1 << src2
        elif opcode == 0xD:
            if not 0 <= src2 < 32:
                raise InvalidCommandError()
            msb = src1 >> 31
            bitmask = ~((-msb) << src2) << (32-src2) if msb else 0
            result = (src1 >> src2) | bitmask
        elif opcode == 0xE:
            if not 0 <= src2 < 32:
                raise InvalidCommandError()
            result = src1 >> src2
        elif opcode == 0xF:
            if not 0 <= src2 < 32:
                raise InvalidCommandError()
            result = src1 >> src2 | src1 << (32-src2)

        negative = result & Cpu.__high != 0
        zero = result == 0
        carry = result & Cpu.__mask != result
        overflow = src1 & Cpu.__high == src2 & Cpu.__high and src1 & Cpu.__high != result & Cpu.__high

        flags = [zero, negative, carry, overflow]

        return flags, result & Cpu.__mask

    @staticmethod
    @purefunction
    def fetchFromRom(rom, address):
        assert not address < 0
        assert address & Cpu.__high != Cpu.__high
        return Cpu.__int8to32(rom[address:address + 4])

    @staticmethod
    @purefunction
    def __getParamsMem(command):
        store = command & 0x20000000 != 0
        rdest = (command & 0x1E000000) >> 25
        op2 = command & 0x01FFFFFF
        return store, rdest, op2
