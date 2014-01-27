#!/usr/bin/env python2
import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)) + "/../")
import assembler
import struct
from emulator import Cpu


class DummyCpu(object):
    ram = []
    rom = []
    pc = 0
    flags = [False] * 4
    register = [0] * 16

    def tick(self):
        return False

    def load(self, _):
        return ""

    def reset(self):
        pass


class Debugger(object):
    breakpoints = []

    def __init__(self, cpu):
        self.cpu = cpu
        self.__fileassoc = {}
        self.__romassoc = {}

    @staticmethod
    def loadFromFile(filename, memorysize=1024*1024):
        """
        Creates a new debugger object
        with the program contents from the given file.
        If it's a debug file, evertyhing will be properly set.
        If not a disaasmbled file will be generated
        """
        assert isinstance(filename, str)
        assert isinstance(memorysize, (int, long))
        result = Debugger(None)
        if filename.endswith(".dbg"):
            with open(filename.rsplit('.', 1)[0]) as code: #that't the .out file
                result.cpu = Cpu(memorysize, code.read())
            with open(filename.rsplit('.', 2)[0]) as content: #the .s file
                result.__filecontent = content.read()
            with open(filename) as debug:
                for line in debug:
                    (key, val) = line.split()
                    result.__romassoc[int(key)] = int(val)
                    result.__fileassoc[int(val)] = int(key)
        elif filename.endswith(".out"):
            with open(filename) as code:
                result.cpu = Cpu(code.read(), memorysize)
            result.__filecontent = ""  #FIXME get disassmbled file

        return result

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
    def Z(self):
        return self.flags[0]
    @Z.setter
    def Z(self, value):
        self.flags[0] = value

    @property
    def N(self):
        return self.flags[1]
    @N.setter
    def N(self, value):
        self.flags[1] = value

    @property
    def C(self):
        return self.flags[2]
    @C.setter
    def C(self, value):
        self.flags[2] = value

    @property
    def V(self):
        return self.flags[3]
    @V.setter
    def V(self, value):
        self.flags[3] = value

    @property
    def register(self):
        return self.cpu.register

    def step(self):
        return self.cpu.tick()

    def run(self):
        while self.step():
            if self.cpu.pc in self.breakpoints:
                return True
        return False

    def __getCommand(self, command):
        bytes = struct.pack(">I", command)
        string = assembler.getTextOfEncodedCommand(bytes)
        return string if string else ""

    def getNextCommand(self):
        return self.__getCommand(self.cpu.load(self.pc))

    def stepOver(self):
        if not self.getNextCommand().startswith('call'): # FIXME: get rid of getnextcommand
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

    def fileContent(self): #TODO: make nice names!
        return self.__filecontent

    def getContentLine(self, pc):
        return self.__fileassoc.get(pc, -1)

    def getRomAddr(self, line):
        return self.__romassoc.get(line, -1)
