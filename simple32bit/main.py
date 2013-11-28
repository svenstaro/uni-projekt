#! /usr/bin/env python2.7

from myhdl import *
from register import *

def Main():
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=False)
    we = Signal(bool(1))
    y = Signal(intbv(11284)[16:])
    x = Signal(intbv(0)[16:])

    dut = register(clock, reset, we, y, x)

    @always(delay(1))
    def clkgen():
        clock.next = not clock

    @instance
    def stimulus():
        reset.next = True
        yield delay(2)
        reset.next = False

        for i in xrange(16):
            yield clock.negedge
            print("%3d  %s" % (now(), bin(x, 16)))

        raise StopSimulation

    return dut, clkgen, stimulus

if __name__ == '__main__':
    m = traceSignals(Main)
    sim = Simulation(m)
    sim.run()

