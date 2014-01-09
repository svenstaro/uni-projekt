import sys
import time

sys.path.append("/home/marcel/studium/WISE1314/Projekt/")
sys.path.append("/home/marcel/studium/WISE1314/Projekt/assembler/")
sys.path.append("/home/marcel/studium/WISE1314/Projekt/assembler/operations/")

import mk, struct, os
from myhdl import *
from allimport import *

class DutClass():
    """Wrapper around DUT"""
    def __init__(self, data=()):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(0, 1, True)
        self.buttons, self.leds = [Signal(intbv(0)[4:]) for _ in range(2)]
        self.data = data
        self.interesting = []
        self.args = [self.clk, self.reset, self.buttons, self.leds, self.data, self.interesting]

    def Gens(self, trace = False):
        result = traceSignals(mk.mk, *self.args) if trace else mk.mk(*self.args)
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
        d = DutClass(data)
        conversion.analyze.simulator = 'icarus'
        conversion.analyze(mk.mk, *d.args)

    def run():
        sim = genSim(verify,data=data,trace=True)
        sim.run()

    # analyze()
    run()
