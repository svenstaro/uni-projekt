from myhdl import *
from allimport import *

def mk(clk, reset, romContent=()):
    """ Oh crap! """

    ### the overall bbus
    bbus = TristateSignal(intbv(0)[32:])

    ### irdecoder
    enIr = Signal(bool(0))
    irAluop, irDest, irSource, irSource2 = [Signal(intbv(0)[4:]) for _ in range(4)]
    irOp1, irOp2, irSup = [Signal(bool(0)) for _ in range(3)]
    irImm24 = Signal(intbv(0)[24:])
    irImm16 = Signal(intbv(0)[16:])
    irJumpOp = Signal(intbv(0)[5:])
    irPrefix = Signal(intbv(0)[5:])

    def createIR():
        _ir2idecoder = Signal(intbv(0)[32:])

        ir = registerr(clk, reset, enIr, bbus, _ir2idecoder)
        irdec = irdecoder(_ir2idecoder, irAluop, irDest, irSource, irOp1, irOp2, irSource2, irImm24, irImm16, irSup, irPrefix, irJumpOp)

        return ir, irdec


    ### cpu
    addrymux1, addrymux0, pmux = [Signal(bool(0)) for _ in range(3)]
    bufAddr, bufOp2, bufAddr14, bufRy, bufAlu, bufPC = [Signal(bool(0)) for _ in range(6)]
    enIr, enPc, enReg, enJump, enCall, enSup = [Signal(bool(0)) for _ in range(6)]
    enMRR, enMAR, enMDR, MRRbuf, MDRbuf, mWe, mOe = [Signal(bool(0)) for _ in range(7)]

    def createCPU():
        Cpu = cpu(clk, reset, irPrefix,
                  addrymux1, addrymux0, pmux,
                  bufAddr, bufOp2, bufAddr14, bufRy, bufAlu, bufPC,
                  enIr, enPc, enReg, enJump, enCall, enSup,
                  enMRR, enMDR, enMAR, MRRbuf, MDRbuf, mWe, mOe)
        return Cpu


    ### statusflags
    zIn, zOut, nIn, nOut, cIn, cOut, vIn, vOut = [Signal(bool(0)) for _ in range(8)]
    sUp = Signal(bool(0))

    def createStatusFlags():
        supAnd = andd(irSup, enSup, sUp)

        Z = registerr(clk, reset, sUp, zIn, zOut, bitwidth=1)
        N = registerr(clk, reset, sUp, nIn, nOut, bitwidth=1)
        C = registerr(clk, reset, sUp, cIn, cOut, bitwidth=1)
        V = registerr(clk, reset, sUp, vIn, vOut, bitwidth=1)
        return supAnd, Z, N, C, V


    ### registerbank
    rgX, rgY = [Signal(intbv(0)[32:]) for _ in range(2)]

    def createRegisterBank():
        yMuxOut = Signal(intbv(0)[4:])
        zMuxOut = Signal(intbv(0)[4:])
        const15 = Signal(intbv(15)[4:])
        const14 = Signal(intbv(14)[4:])
        const15.driven = True #suppress some warnings
        const14.driven = True

        yMux = mux41(addrymux1, addrymux0, irSource2, const15, const14, irDest, yMuxOut)
        zMux = mux41(addrymux1, addrymux0, irDest, const15, const14, irSource2, zMuxOut)
        rb = registerbank(clk, enReg, irSource, yMuxOut, zMuxOut, rgX, rgY, bbus)
        ryTristate = tristate(rgY, bufRy, bbus.driver())
        return yMux, zMux, rb, ryTristate


    ### alu

    def createALUBuf():
        BmuxOut = Signal(intbv(0)[32:])
        aluRes = Signal(intbv(0)[32:])

        Bmux = mux21(irOp2, rgY, irImm16, BmuxOut)
        Alu = alu(irAluop, rgX, BmuxOut, cOut, aluRes, zIn, nIn, cIn, vIn)
        aluTristate = tristate(aluRes, bufAlu, bbus.driver())
        return Bmux, Alu, aluTristate


    ### jumpunit
    jumpResult = Signal(bool(0))

    def createJumpUnit():
        ju = jumpunit(irJumpOp, zOut, nOut, cOut, vOut, jumpResult)
        return ju


    ### programmcounter
    pcOut = Signal(intbv(0)[32:])

    def createPcBuf():
        pc = programcounter(clk, reset, enPc, irImm24, rgY, enCall, jumpResult, enJump, irOp1, pcOut)
        pcTristate = tristate(pcOut, bufPC, bbus.driver())

        return pc, pcTristate


    ### push/pop addr calc

    def createAddr14Buf():
        const_5 = Signal(intbv(-4)[32:])
        const4 = Signal(intbv(4)[32:])
        const_5.driven = True
        const4.driven  = True

        plusminusMuxOut = Signal(intbv(0)[32:])
        addr14 = Signal(modbv(0)[32:])

        plusminusMux = mux21(pmux, const_5, const4, plusminusMuxOut)
        add = adder(plusminusMuxOut, rgY, addr14)
        addr14tristate = tristate(addr14, bufAddr14, bbus.driver())

        return plusminusMux, add, addr14tristate


    ### op2buf

    def createOp2Buf():
        op2muxOut = Signal(intbv(0)[32:])

        op2mux = mux21(irOp1, rgY, irImm24, op2muxOut)
        op2tristate = tristate(op2muxOut, bufOp2, bbus.driver())

        return op2mux, op2tristate

    ### addrbuf

    def createAddrBuf():
        addOut = Signal(modbv(0)[32:])
        addrMuxOut = Signal(intbv(0)[32:])

        add = adder(pcOut, irImm24, addOut)
        addrMux = mux21(irOp1, rgY, addOut, addrMuxOut)
        addrTristate = tristate(addrMuxOut, bufAddr, bbus.driver())

        return add, addrMux, addrTristate

    ### RAM/ROM
    membus = TristateSignal(intbv(0)[32:])
    memaddr = Signal(intbv(0)[32:])

    def createMAR():
        mar = registerr(clk, reset, enMAR, bbus, memaddr)

        return mar

    def createMDR():
        mdr2tristate = Signal(intbv(0)[32:])

        mdr = registerr(clk, reset, enMDR, bbus, mdr2tristate)
        mdrTristate = tristate(mdr2tristate, MDRbuf, membus.driver())

        return mdr, mdrTristate

    def createMRR():
        mrr2tristate = Signal(intbv(0)[32:])

        mrr = registerr(clk, reset, enMRR, membus, mrr2tristate)
        mrrTristate = tristate(mrr2tristate, MRRbuf, bbus.driver())

        return mrr, mrrTristate

    def createMemory():
        #TODO just use the first n bits of the addr for the ram/rom
        outputE, outputW, msbSig, msbSigI= [Signal(bool(0)) for _ in range(4)]

        msbSignSelector = selectBit(memaddr, msbSig, 31)
        msbSignNegate = negation(msbSig, msbSigI)

        ffmOe = dff(clk, mOe, outputE)
        ffmWe = dff(clk, mWe, outputW)

        ram = pseudoram(clk, outputW, outputE, msbSig, memaddr, membus, membus.driver())
        rom = pseudorom(mOe, msbSigI, memaddr, membus.driver(), romContent) #TODO swap msbSig

        return msbSignSelector, msbSignNegate, ffmOe, ffmWe, ram, rom

    result = createIR(), createCPU(), createStatusFlags(), createRegisterBank(), createALUBuf(), createJumpUnit(), createPcBuf(), createAddr14Buf(), createOp2Buf(), createAddrBuf(),\
             createMAR(), createMDR(), createMRR(), createMemory()

    return result
