#!/usr/bin/env python2
import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)) + "/../")
import assembler
import struct
from emulator import Cpu

class Debugger(object):
    breakpoints = []

    def __init__(self, program, memorysize=1024*1024):
        self.cpu = Cpu(memorysize, program)

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
        result = None
        if filename.endswith(".dbg"):
            with open(filename.rsplit('.', 1)[0]) as code: #that't the .out file
                result = Debugger(code.read(), memorysize)
            with open(filename.rsplit('.', 2)[0]) as content: #the .s file
                result.__filecontent = content.read()
            with open(filename) as debug:
                result.__fileassoc = {}
                result.__romassoc = {}
                for line in debug:
                    (key, val) = line.split()
                    result.__romassoc[int(key)] = int(val)
                    result.__fileassoc[int(val)] = int(key)
        elif filename.endswith(".out"):
            with open(filename) as code:
                result = Debugger(code.read(), memorysize)
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
        return self.__fileassoc[pc]

    def getRomAddr(self, line):
        return self.__romassoc[line]

    def hasReachedEnd(self):
        return self.getNextCommand() == 'halt'

