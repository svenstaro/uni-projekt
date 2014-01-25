from myhdl import *
from allimport import *

def processor(clk, reset,
              buttons, leds,
              rx, tx,
              memoryaddr, memoryin, memoryout,
              romrden, ramrden, ramwren,
              fifodata, fifore, fifowe, fifoempty, fifofull, fifoq,
              baudrate=57600, enCache=True, interesting=None):
    """
    clk        (Ibool)  -- The clock
    reset      (IReset) -- Reset Signal
    buttons    (I4)     -- 4 input buttons
    leds       (O4)     -- 4 output LEDS
    rx         (Ibool)  -- input from rs232
    tx         (Obool)  -- output from rs232
    memoryaddr (O16)    -- memory addr
    memoryin   (I32)    -- memory read
    memoryout  (O32)    -- memory write
    romrden    (Obool)  -- rom-readenable
    ramrden    (Obool)  -- ram-readenable
    ramwren    (Obool)  -- ram-writeenable
    fifodata   (O8)     -- fifo data in
    fifore     (Obool)  -- enable reading from fifo
    fifowe     (Obool)  -- enable writing to fifo
    fifoempty  (Ibool)  -- indicates, that fifo is empty
    fifofull   (Ibool)  -- indicates, that the fifo is full
    fifoq      (I8)     -- fifo data out

    baudrate           -- the baudrate for the rs232
    enCache            -- enable cache or not
    interesting        -- A list with interesting signals will be returned
    """


    ### the actual bus
    bbus = TristateSignal(intbv(0)[32:])

    ### irdecoder
    enIr = Signal(bool(0))
    irAluop, irDest, irSource, irSource2 = [Signal(intbv(0)[4:]) for _ in range(4)]
    irOp1, irOp2, irSup = [Signal(bool(0)) for _ in range(3)]
    irImm24 = Signal(intbv(0)[24:])
    irImm16 = Signal(intbv(0)[16:])
    irJumpOp = Signal(intbv(0)[5:])
    irPrefix = Signal(intbv(0)[7:])

    def createIR():
        ir2idecoder = Signal(intbv(0)[32:])

        ir = registerr(clk, reset, enIr, bbus, ir2idecoder)
        irdec = irdecoder(ir2idecoder, irAluop, irDest, irSource, irOp1, irOp2, irSource2, irImm24, irImm16, irSup, irPrefix, irJumpOp)

        return ir, irdec


    ### cpu
    readybit, rstreadybit = [Signal(bool(1)) for _ in range(2)]  # they must be true!
    addrymux1, addrymux0, pmux = [Signal(bool(0)) for _ in range(3)]
    bufAddr, bufOp2, bufAddr14, bufRy, bufAlu, bufPC, bufClk, bufBut, bufRsr = [Signal(bool(0)) for _ in range(9)]
    enAlu, enIr, enPc, enReg, enJump, enCall, enSup, enLed, enRst = [Signal(bool(0)) for _ in range(9)]
    enMmu, mmuBuf = [Signal(bool(0)) for _ in range(2)]

    def createCPU():
        ffavail = Signal(bool(0))

        ffneg = negation(fifoempty, ffavail)
        ffread = aA(bufRsr, False, fifore)
        Cpu = cpu(clk, reset, irPrefix, readybit, ffavail, rstreadybit,
                  addrymux1, addrymux0, pmux,
                  bufAddr, bufOp2, bufAddr14, bufRy, bufAlu, bufPC, bufClk, bufBut, bufRsr,
                  enAlu, enIr, enPc, enReg, enJump, enCall, enSup, enLed, enRst,
                  enMmu, mmuBuf)

        return ffneg, ffread, Cpu


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

        yMux = mux41(addrymux1, addrymux0, irSource2, 15, 14, irDest, yMuxOut)
        zMux = mux41(addrymux1, addrymux0, irDest, 15, 14, irSource2, zMuxOut)
        rb = registerbank(clk, reset, enReg, irSource, yMuxOut, zMuxOut, rgX, rgY, bbus)
        ryTristate = tristate(rgY, bufRy, bbus)

        return yMux, zMux, rb, ryTristate


    ### alu

    def createALUBuf():
        BmuxOut = Signal(intbv(0)[32:])
        aluRes = Signal(modbv(0)[32:])

        Bmux = mux21(irOp2, rgY, irImm16, BmuxOut)
        Alu = alu(irAluop, enAlu, rgX, BmuxOut, cOut, aluRes, zIn, nIn, cIn, vIn)
        aluTristate = tristate(aluRes, bufAlu, bbus)

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
        pcTristate = tristate(pcOut, bufPC, bbus)

        return pc, pcTristate


    ### push/pop addr calc

    def createAddr14Buf():
        plusminusMuxOut = Signal(modbv(0)[32:])
        addr14 = Signal(modbv(0)[32:])

        plusminusMux = mux21(pmux, -4, 4, plusminusMuxOut)
        add = adder(plusminusMuxOut, rgY, addr14)
        addr14tristate = tristate(addr14, bufAddr14, bbus)

        return plusminusMux, add, addr14tristate


    ### op2buf

    def createOp2Buf():
        op2muxOut = Signal(intbv(0)[32:])

        op2mux = mux21(irOp1, rgY, irImm24, op2muxOut)
        op2tristate = tristate(op2muxOut, bufOp2, bbus)

        return op2mux, op2tristate

    ### addrbuf

    def createAddrBuf():
        addOut = Signal(modbv(0)[32:])
        addrMuxOut = Signal(intbv(0)[32:])

        add = adder(pcOut, irImm24, addOut)
        addrMux = mux21(irOp1, rgY, addOut, addrMuxOut)
        addrTristate = tristate(addrMuxOut, bufAddr, bbus)

        return add, addrMux, addrTristate


    ### clkbuf

    def createClkBuf():
        clkOut = Signal(intbv(0)[32:])

        clkTristate = tristate(clkOut, bufClk, bbus)
        clock = counter(clk, reset, True, clkOut)

        return clkTristate, clock

    ### rs232

    def createRs232():
        readerTristate = tristate(fifoq, bufRsr, bbus)

        writer = rs232tx(clk, reset, rstreadybit, enRst, bbus, tx, baudRate=baudrate)
        reader = rs232rx(clk, reset, fifowe, fifodata, rx, baudRate=baudrate)

        return readerTristate, reader, writer

    ### hardware

    def createLedBut():
        ioOut = Signal(intbv(0)[32:])

        io = iodevice(clk, reset, enLed, ioOut, bbus, leds, buttons)
        ioTristate = tristate(ioOut, bufBut, bbus)

        return io, ioTristate

    ### MMU

    def createMmu():
        enO, enW, csA, csO= [Signal(bool(0)) for _ in range(4)]

        # romaddr, romclk, romrden, romout,
        mmuOut = Signal(intbv(0)[32:])
        enableromout = andd(enO, csO, romrden)
        enableramout = andd(enO, csA, ramrden)
        enableramwri = andd(enW, csA, ramwren)

        Mmu = mmu(clk, reset, enMmu, bbus, mmuOut, readybit, memoryaddr, memoryin, memoryout, enO, enW, csA, csO, False)
        mmuTristate = tristate(mmuOut, mmuBuf, bbus)

        return enableromout, enableramout, enableramwri, Mmu, mmuTristate

    if interesting is not None:
        interesting.append(bbus)

    IR = createIR()
    CPU = createCPU()
    StatusFlags = createStatusFlags()
    RegisterBank = createRegisterBank()
    ALU = createALUBuf()
    JumpUnit = createJumpUnit()
    PC = createPcBuf()
    Addr14Buf = createAddr14Buf()
    Op2Buf = createOp2Buf()
    AddrBuf = createAddrBuf()
    ClkBuf = createClkBuf()
    RS232 = createRs232()
    IO = createLedBut()
    Memory = createMmu()

    return instances()
