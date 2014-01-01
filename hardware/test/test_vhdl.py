from myhdl import *
from hardware.allimport import *

def verify(dut, *args):
    assert not conversion.analyze(dut, *args)

def verifyALU():
    opc = Signal(intbv(0)[4:])
    A, B, R = [Signal(intbv(0)[32:]) for _ in range(3)]
    en, Cin, Z, N, C, V = [Signal(bool(0)) for _ in range (6)]

    verify(alu, opc, en, A, B, Cin, R, Z, N, C, V)

def verifyCpu():
    clk = Signal(bool(0))
    reset = ResetSignal(0, 1, True)
    addr = Signal(intbv(0)[5:])
    addrymux1, addrymux0, pmux = [Signal(bool(0)) for _ in range(3)]
    bufAddr, bufOp2, bufAddr14, bufRy, bufAlu, bufPC = [Signal(bool(0)) for _ in range(6)]
    enAlu, enIr, enPc, enReg, enJump, enCall, enSup = [Signal(bool(0)) for _ in range(7)]
    enMRR, enMAR, enMDR, MRRbuf, MDRbuf, mWe, mOe = [Signal(bool(0)) for _ in range(7)]

    verify(cpu, clk, reset, addr, addrymux1, addrymux0, pmux, bufAddr, bufOp2, bufAddr14, bufRy, bufAlu, bufPC,
           enAlu, enIr, enPc, enReg, enJump, enCall, enSup, enMRR, enMAR, enMDR, MRRbuf, MDRbuf, mWe, mOe)

def verifyIrDecoder():
    ir = Signal(intbv(0)[32:])
    enIr = Signal(bool(0))
    Aluop, Dest, Source, Source2 = [Signal(intbv(0)[4:]) for _ in range(4)]
    Op1, Op2, Sup = [Signal(bool(0)) for _ in range(3)]
    Imm24 = Signal(intbv(0)[24:])
    Imm16 = Signal(intbv(0)[16:])
    JumpOp = Signal(intbv(0)[5:])
    Prefix = Signal(intbv(0)[5:])

    verify(irdecoder, ir, Aluop, Dest, Source, Op1, Op2, Source2, Imm24, Imm16, Sup, Prefix, JumpOp)

if __name__ == '__main__':
    verify(adder, Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(modbv(0)[32:]))
    verify(addrdecoder, Signal(intbv(0)[32:]), Signal(bool(0)), Signal(bool(0)))
    verifyALU()
    verify(counter, Signal(bool(0)), ResetSignal(0, 1, True), Signal(bool(0)), Signal(intbv(0)[32:]))
    verifyCpu()
    verify(dff, Signal(bool(0)), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]))
    verifyIrDecoder()
    verify(jumpunit, Signal(intbv(0)[5:]), Signal(bool(0)), Signal(bool(0)), Signal(bool(0)), Signal(bool(0)), Signal(bool(0)))
    verify(mux41, Signal(bool(0)), Signal(bool(0)), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]))
    verify(mux21, Signal(bool(0)), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]))
    verify(programcounter, Signal(bool(0)), ResetSignal(0, 1, True), Signal(bool(0)), Signal(intbv(0)[24:]), Signal(intbv(0)[32:]), Signal(bool(0)), Signal(bool(0)), Signal(bool(0)), Signal(bool(0)), Signal(intbv(0)[32:]))
    verify(pseudoram, Signal(bool(0)), Signal(bool(0)), Signal(bool(0)), Signal(bool(0)), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]))
    verify(pseudorom, Signal(bool(0)), Signal(bool(0)), Signal(intbv(0)[8:]), Signal(intbv(0)[4:]), (0, 0, 0))
    verify(registerr, Signal(bool(0)), ResetSignal(0, 1, True), Signal(bool(0)), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]))
    verify(registerbank, Signal(bool(0)), Signal(bool(0)), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]), Signal(intbv(0)[32:]))
    verify(selectBit, Signal(intbv(0)[32:]), Signal(bool(0)), 3)
    verify(tristate, Signal(intbv(0)[32:]), Signal(bool(0)), TristateSignal(intbv(0)[32:]).driver())
