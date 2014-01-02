import sys

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
        self.data = data
        self.bus = TristateSignal(intbv(0)[32:])
    def Gens(self, trace = False):
        args = [self.clk, self.reset, self.data, self.bus]

        return traceSignals(mk.mk, *args) if trace else mk.mk(*args)

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
                raise StopSimulation("HALT DETECTED")
            elif (not (cl.bus._val is None)) and cl.bus[32:26] == 0b111110: #swi
                yield cl.clk.posedge
                yield cl.clk.posedge
                yield cl.clk.posedge
                print "SWI: " + str(cl.bus)

    #     d = DutClass(data)
    #     conversion.analyze(mk.mk, d.clk, d.reset, d.data
    sim = genSim(verify,data=data,trace=True)
    sim.run()
