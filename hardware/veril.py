import sys
sys.path.append("/home/marcel/studium/WISE1314/Projekt/")

import struct
import os
from myhdl import *
from argparse import ArgumentParser
import c25Board

class DutClass():
    """Wrapper around DUT"""
    def __init__(self, data):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(0, 1, True)
        self.buttons, self.leds = [Signal(intbv(0)[4:]) for _ in range(2)]
        self.rx, self.tx = [Signal(intbv(0)[8:]) for _ in range(2)]
        self.data = data
        self.args = [self.clk, self.reset, self.buttons, self.leds, self.rx, self.tx, self.data]

def genSim(verifyMethod, dut_cl, clkfreq=1, trace=False):
    """ Generates a Simulation Object """

    dut = traceSignals(c25Board.c25Board, *dut_cl.args) if trace else c25Board.c25Board(*dut_cl.args)

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
    def analyzeBoard(dut_cl):
        conversion.analyze.simulator = 'icarus'
        conversion.analyze(c25Board.c25Board, *dut_cl.args)

    def compileBoard(dut_cl):
        conversion.toVerilog.name = 'c25Board'
        conversion.toVerilog.no_testbench = True
        conversion.toVerilog(c25Board.c25Board, *dut_cl.args)

    def run(dut_cl, trace):
        def verify(cl, _):
            while True:
                yield cl.clk.posedge
                if bus == 0b01000011111111111111111111111100: #halt
                    raise StopSimulation("HALT DETECTED (%s)" % now())
                elif bus._val is not None and bus[32:26] == 0b111110: #swi
                    yield cl.clk.posedge
                    yield cl.clk.posedge
                    yield cl.clk.negedge
                    print "SWI (%s): %s" % (now(), str(bus._val))

        interesting=[]
        dut_cl.args.append(interesting)
        sim = genSim(verify, dut_cl, trace=trace)
        bus = interesting[0]
        sim.run()

    parser = ArgumentParser(description='C25Board emulator and generator')
    parser.add_argument('filename', type=str, nargs=1, help='a executable')
    parser.add_argument('--type', choices=['analyze', 'compile', 'run'], default='run', help='specify the type')
    parser.add_argument('--trace', action='store_true', help='enable tracing?')
    parser.add_argument('--nocache', action='store_false', help='disable cache')

    args = parser.parse_args()

    with open(args.filename[0]) as f:
        size = os.path.getsize(f.name)//4
        data = struct.unpack('>' + "I"*size, f.read(4*size))


    dut_cl = DutClass(data)

    #we currently have a bug with the cache, so nocache will be enforced!
    args.nocache = False

    dut_cl.args.append(args.nocache)

    if args.type == 'analyze':
        analyzeBoard(dut_cl)
    elif args.type == 'compile':
        compileBoard(dut_cl)
    elif args.type == 'run':
        run(dut_cl, args.trace)
