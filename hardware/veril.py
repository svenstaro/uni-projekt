import sys
import time

sys.path.append("/home/marcel/studium/WISE1314/Projekt/")
sys.path.append("/home/marcel/studium/WISE1314/Projekt/assembler/")
sys.path.append("/home/marcel/studium/WISE1314/Projekt/assembler/operations/")

import c25Board, struct, os
from myhdl import *
from allimport import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self, data=(), converse=False):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(0, 1, True)
        self.buttons, self.leds = [Signal(intbv(0)[4:]) for _ in range(2)]
        self.data = data
        self.args = [self.clk, self.reset, self.buttons, self.leds, self.data]
        self.converse = converse

        if not self.converse:
            self.interesting = []
            self.args.append(self.interesting)


    def Gens(self, trace = False):
        result = traceSignals(c25Board.c25Board, *self.args) if trace else c25Board.c25Board(*self.args)

        if not self.converse:
            self.bus = self.interesting[0]
            self.ready = self.interesting[1]

        return result


def genSim(verifyMethod, cl=DutClass, clkfreq=1, trace=False, data=()):
    """ Generates a Simulation Object """

    dut_cl = cl(data)
    dut = dut_cl.Gens(trace=trace)

    @always(delay(clkfreq))
    def clkGen():
        #time.sleep(0.05)
        dut_cl.clk.next = not dut_cl.clk

    @instance
    def stimulus():
        dut_cl.reset.next = True
        yield delay(3*clkfreq)
        dut_cl.reset.next = False

        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    return Simulation(dut, clkGen, stimulus)

if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            size = os.path.getsize(f.name)//4
            data = struct.unpack('>' + "I"*size, f.read(4*size))
    except IndexError:
        print "Supply a filename!"
        sys.exit(1)

    def verify(cl, dut):
        while True:
            yield cl.clk.posedge
            if cl.bus == 0b01000011111111111111111111111100: #halt
                raise StopSimulation("HALT DETECTED (%s)" % now())
            elif cl.bus._val is not None and cl.bus[32:26] == 0b111110: #swi
                yield cl.clk.posedge
                yield cl.clk.posedge
                yield cl.clk.negedge
                print "SWI (%s): %s" % (now(), str(cl.bus._val))

    def analyze():
        d = DutClass(data=data, converse=True)
        conversion.analyze.simulator = 'icarus'
        conversion.analyze(c25Board.c25Board, *d.args)

    def compile():
        d = DutClass(data=data, converse=True)
        conversion.toVerilog.name = 'c25Board'
        conversion.toVerilog.no_testbench = True
        conversion.toVerilog(c25Board.c25Board, *d.args)

    def run():
        sim = genSim(verify,data=data,trace=True)
        sim.run()

    # analyze()
    compile()
    # run()
