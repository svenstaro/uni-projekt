import sys
sys.path.append("/home/marcel/studium/WISE1314/Projekt/")

import struct
import os
from myhdl import *
from argparse import ArgumentParser
from c25Board import c25Board
from rs232 import rs232rx
from pseudorom import pseudorom

class DutClass():
    """Wrapper around DUT"""
    def __init__(self):
        self.clk = Signal(bool(0))
        self.reset = ResetSignal(1, 0, True)
        self.buttons, self.leds = [Signal(intbv(0)[4:]) for _ in range(2)]
        self.rx, self.tx = [Signal(bool(1)) for _ in range(2)]

        self.memoryaddr = Signal(intbv(0)[8:])
        self.memorydata = TristateSignal(intbv(0)[32:])
        self.ramrden, self.ramwren, self.romrden = [Signal(bool(0)) for _ in range(3)]

        self.baudrate = 57600
        self.args = [self.clk, self.reset,
                     self.buttons, self.leds,
                     self.rx, self.tx,
                     self.memoryaddr, self.memorydata,
                     self.romrden, self.ramrden, self.ramwren]

def genSim(verifyMethod, dut_cl, data, *argss, **kwargs):
    """ Generates a Simulation Object """

    dut = traceSignals(c25Board, *dut_cl.args) if kwargs.get('trace', False) else c25Board(*dut_cl.args)

    @always(delay(kwargs.get('clkfreq', 1)))
    def clkGen():
        #time.sleep(0.05)
        dut_cl.clk.next = not dut_cl.clk

    @instance
    def stimulus():
        dut_cl.reset.next = False
        yield delay(3*kwargs.get('clkfreq', 1))
        dut_cl.reset.next = True

        yield verifyMethod(dut_cl, dut)
        raise StopSimulation

    rom = pseudorom(dut_cl.clk, dut_cl.romrden, dut_cl.romrden, dut_cl.memoryaddr, dut_cl.memorydata, mem=data)

    return Simulation(dut, clkGen, stimulus, rom, *argss)






if __name__ == "__main__":
    def analyzeBoard(dut_cl):
        conversion.analyze.simulator = 'icarus'
        conversion.analyze(c25Board, *dut_cl.args)

    def compileBoard(dut_cl):
        conversion.toVerilog.no_testbench = True
        conversion.toVerilog(c25Board, *dut_cl.args)

    def run(dut_cl, trace):
        def verify(cl, _):
            assert isinstance(cl, DutClass)

            while True:
                yield cl.clk.posedge
                if bus._val is not None:
                    if bus[32:26] == 0b111110: #led
                        yield cl.clk.posedge
                        yield cl.clk.posedge
                        yield cl.clk.negedge
                        print "LEDS (%s): %s" % (now(), str(~cl.leds._val))
                    elif bus[32:26] == 0b111111: #rst
                        yield rs232avail.posedge
                        rs232read.next = True
                        yield cl.clk.posedge
                        rs232read.next = False
                        sys.stdout.write(chr(rs232out))
                        sys.stdout.flush()

        @always(dut_cl.clk.posedge)
        def stop():
            if bus == 0b01000011111111111111111111111100: #halt
                raise StopSimulation("HALT DETECTED (%s)" % now())

        interesting=[]
        dut_cl.args.append(interesting)
        rs232avail = Signal(True)
        rs232read = Signal(False)
        rs232out = Signal(intbv(0)[8:])
        rs232read = rs232rx(dut_cl.clk, dut_cl.reset, rs232avail, rs232out, dut_cl.tx, baudRate=dut_cl.baudrate)
        sim = genSim(verify, dut_cl, data, rs232read, stop, trace=trace)
        bus = interesting[0]
        sim.run()

    parser = ArgumentParser(description='C25Board emulator and generator')
    parser.add_argument('filename', type=str, nargs=1, help='a executable')
    parser.add_argument('--type', choices=['analyze', 'compile', 'run'], default='run', help='specify the type')
    parser.add_argument('--trace', action='store_true', help='enable tracing')
    parser.add_argument('--nocache', action='store_false', help='disable cache')
    parser.add_argument('--baudrate', type=int, default=57600, help='baudrate for rs232')

    args = parser.parse_args()

    with open(args.filename[0]) as f:
        size = os.path.getsize(f.name)
        data = struct.unpack('>' + "B"*size, f.read(size))

    dut_cl = DutClass()
    dut_cl.args.append(args.baudrate)
    dut_cl.baudrate = args.baudrate

    #we currently have a bug with the cache, so nocache will be enforced!
    args.nocache = False

    dut_cl.args.append(args.nocache)

    if args.type == 'analyze':
        analyzeBoard(dut_cl)
    elif args.type == 'compile':
        compileBoard(dut_cl)
    elif args.type == 'run':
        run(dut_cl, args.trace)
