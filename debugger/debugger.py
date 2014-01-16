#!/usr/bin/env python2
import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)) + "/../")
import assembler
from emulator import Cpu


class Debugger(object): 
    breakpoints = []

    def __init__(self, program, memorysize=1024*1024):
        self.cpu = Cpu(memorysize, program)

    @staticmethod
    def loadFromFile(filename, memorysize=1024*1024):
        with open(filename) as fin:
            return Debugger(fin.read(), memorysize)

    @property
    def pc(self):
        return self.cpu.pc
    @pc.setter
    def pc(self, value):
        self.cpu.pc = value

    @property
    def ram(self):
        return self.cpu.ram

    @property
    def rom(self):
        return self.cpu.rom

    @property
    def flags(self):
        return self.cpu.flags

    @property
    def register(self):
        return self.cpu.register

    def step(self):
        return self.cpu.tick()

    def run(self):
        while self.step():
            if self.cpu.pc in breakpoints:
                return True
        return False

    def getNextCommand(self):
        return assembler.getTextOfEncodedCommand(self.rom[self.pc])

    def stepOver(self):
        if not self.getNextCommand().startsWith('call'):
            return self.step()

        self.breakpoints.append(self.pc+4)
        result = self.run()
        self.breakpoints.pop()
        return result

    __flag_order = 'ZNCO'

    def reset(self):
        self.cpu.reset()

    def __str__(self):
        s = "PC:  0x%s\n" % hex(self.pc)[2:].zfill(8)
        s += "Flags:     %s\n" % ''.join(s if n else ' ' for s,n in zip(self.__flag_order, self.flags))
        rs = [("$%s"%i).rjust(3) + ": " + (" %s" % hex(v)).rjust(10) for i,v in enumerate(self.register)]
        r = ['  '.join((a,b)) for a,b in zip(rs[:8], rs[8:])]
        s += "Register:\n" + '\n'.join(r)
        return s
