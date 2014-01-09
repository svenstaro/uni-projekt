#!/usr/bin/env python2
import sys
import os
from cpu import Cpu
import cpu
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from assembler import getTextOfCommand

class Emulator(object): 

    def __init__(self):
        self.waiting_at = False
        self.cpu = False

    def printpretty(self, n):
        suffixes = [" ", " k", " M", " G", " T"]
        order = 0
        while n > 1000 and order < len(suffixes) - 1:
            n /= 1000.0
            order += 1
        suffix = suffixes[order]

        return str(int(n)) + "." + str(int(n*100) % 100) + suffix  # TODO iih

    # runs a whole read in program
    def run(self, program_contents):
        cpu = Cpu(1024*1024, program_contents)
        start = time.time()
        cpu.run()
        end = time.time()
        print
        print "Executed %sops in %ss ( %sops/sec )" % (self.printpretty(cpu.counter),
                                                   self.printpretty(end - start),
                                                   self.printpretty(cpu.counter / (end - start)))

    # performs a single cpu step. Returns true, if the program has not terminated yet, 
    # but if the EOF is reached, False is returned.
    def step(self, program_contents):
        if self.cpu == False:
            self.cpu = Cpu(1024*1024, program_contents)
        if self.waiting_at == False:
            self.last_pc = self.waiting_at
            self.waiting_at = self.cpu.step()
        else:
            self.last_pc = self.waiting_at
            self.waiting_at = self.cpu.step(self.waiting_at)
        if(self.waiting_at == False):
            return False
        return True

    # reads the provided file into the system, returns read in contents.
    def readIn(self, fp):
        program_contents = ""
        while True:
            read = os.read(fp, 4096)
            if len(read) == 0:
                break
            program_contents += read
        os.close(fp)
        return program_contents


    def entry_point(self, argv):
        try:
            filename = argv[1]
        except IndexError:
            print "You must supply a filename"
            return 1
        program_contents = readIn(os.open(filename, os.O_RDONLY, 0777))
        run(program_contents)
        return 0


    def target(self, *args):
        return entry_point, None


    def jitpolicy(self, driver):
        from rpython.jit.codewriter.policy import JitPolicy
        return JitPolicy()

    def getFlags(self):
        if self.cpu:
            return self.cpu.getFlags()
        return [False]*4

    def getRegister(self):
        if self.cpu:
            return self.cpu.getRegister()
        return [False]*16

    def stop(self):
        self.cpu.stopExecution()
        self.cpu.reset()
        self.cpu = False
        self.waiting_at = False


    def getLastExecutedCommand(self):
        """Returns the last command that has been executed by the cpu, or an empty string if nothing has been executed."""
        if(self.last_pc != False):
            instruct = cpu.fetchFromRom(self.cpu.rom, self.last_pc)
            return getTextOfCommand(bin(instruct)[2:].zfill(32))
        return ""

    def getNextCommandToExecute(self):
        """Returns the next command that will be executed by the cpu."""
        instruct = cpu.fetchFromRom(self.cpu.rom, self.waiting_at)
        return getTextOfCommand(bin(instruct)[2:].zfill(32))


    

    