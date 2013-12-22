# -*- coding: utf-8 -*-
from ctypes import c_bool
from myhdl import *

def cpu(clk, addr, nextA, nextB, upcmux2, upcmux1, upcmux0, addrx15,
        rxBuf, op2Buf, addrBuf, aluBuf, pcBuf,
        enIr, enZ, enN, enC, enV, enPC, regWe, pcmux1, pcmux0,
        enMRR, enMDR, enMAR, MRRbuf, MDRbuf, mWe, mOe):
    """
        This is a cpu state maschine. Let's see how far we come.
        All parameters are Signals as usual.

        clk     (Ibool) -- The clock
        addr    (I8)    -- Next action
        nextA   (O8)    -- next uPC addr A
        nextB   (O8)    -- next uPC addr B
        upcmux2 (Obool) -- uPCMuxSelector
        upcmux1 (Obool) -- uPCMuxSelector
        upcmux0 (Obool) -- uPCMuxSelector
        addrx15 (Obool) -- set addrx for register to 15 (return addr register)
        rxBuf   (Obool) -- bufbit for xout
        op2Buf  (Obool) -- bufbit for second opcode
        addrBuf (Obool) -- bufbit for addr (pc+imm)
        aluBuf  (Obool) -- bufbit for alu
        pcBuf   (Obool) -- bufbit for pc (programcounter)
        enIr    (Obool) -- enable IR
        enZ     (Obool) -- enable zero-register
        enN     (Obool) -- enable negative-register
        enC     (Obool) -- enable carry-register
        enV     (Obool) -- enable overflow register
        enPC    (Obool) -- enable ProgrammCounter
        regWe   (Obool) -- enable registe write
        pcmux1  (Obool) -- pcMuxSelector
        pcmux0  (Obool) -- pcMuxSelector
        enMRR   (Obool) -- enable MemoryReadRegister
        enMDR   (Obool) -- enable MemoryDataRegister
        enMAR   (Obool) -- enable MemoryAddressRegister
        MRRbuf  (Obool) -- bufbit MemoryReadRegister
        MDRbuf  (Obool) -- bufbit MemoryDataRegister
        mWe     (Obool) -- memoryWriteEnable
        mOe     (Obool) -- memoryOutputEnable
    """

    tState = enum('UNKNOWN', 'FETCH', 'DECODE', 'ALUOP', 'JUMP', 'LOAD', 'STORE', 'ILLEGAL', 'HALT')  # TODO add more
    cState = Signal(tState.FETCH)

    """
        Ich muss noch überlegen, wie ich den bedingten sprung hier rein bekomme.
        Entweder ich switsche nach einer eingangsvariable oder son kack, oder ich
        führe einen upc ein (wie er zur zeit halb vorgesehen ist, aber keine ahnung wie)
    """

    def preset():
        nextA.next = 0
        nextB.next = 0
        upcmux2.next = False
        upcmux1.next = False
        upcmux0.next = False
        addrx15.next = False
        rxBuf.next = False
        addrBuf.next = False
        aluBuf.next = False
        pcBuf.next = False
        enIr.next = False
        enZ.next = False
        enN.next = False
        enC.next = False
        enV.next = False
        regWe.next = False
        enPC.next = False
        pcmux1.next = False
        pcmux0.next = False
        enMRR.next = False
        enMDR.next = False
        enMAR.next = False
        MRRbuf.next = False
        MDRbuf.next = False
        mWe.next = False
        mOe.next = False

    @always(clk.posedge)
    def logic():
        preset() #this is important!

        if   cState == tState.UNKNOWN: #TODO mir gefällt die Lösung mit dem unknown state nicht, mal gucken, ob ich das besser hinbekomme
            if   addr[32:30] == 0b00:
                cState.next = tState.ALUOP
            elif addr[32:30] == 0b11:
                cState.next = tState.JUMP
            elif addr[32:28] == 0b100:
                cState.next = tState.LOAD
            elif addr[32:28] == 0b101:
                cState.next = tState.STORE
            else:
                cState.next = tState.ILLEGAL # TODO add more
        elif cState == tState.FETCH:
            pcBuf.next = True
            enMAR.next = True
            yield clk.posedge
            preset()
            mOe.next = True
            yield clk.posedge #TODO add delay for timing
            preset()
            mOe.next = True
            enMRR.next = True
            yield clk.posedge
            preset()
            MRRbuf.next = True
            enIr.next = True
            cState.next = tState.DECODE
        elif cState == tState.DECODE:
            upcmux2.next = True
            upcmux1.next = True
            upcmux0.next = True
            enPC.next    = True
            cState._next = tState.UNKNOWN
        elif cState == tState.ALUOP:
            enZ.next = True
            enN.next = True
            enC.next = True
            enV.next = True
            aluBuf.next = True
            regWe.next  = True
            cState.next = tState.FETCH
        elif cState == tState.JUMP:
            pass
        elif cState == tState.LOAD:
            pcBuf.next = True
            enMAR.next = True
            yield clk.posedge
            preset()
            mOe.next = True
            yield clk.posedge #TODO add delay for timing
            preset()
            mOe.next = True
            enMRR.next = True
            yield clk.posedge
            preset()
            MRRbuf.next = True
            regWe.next = True
            cState.next = tState.FETCH
        elif cState == tState.STORE:
            rxBuf.next = True
            enMAR.next = True
            yield clk.posedge
            preset()
            op2Buf.next = True
            enMDR.next  = True
            yield clk.posedge
            preset()
            MDRbuf.next = True
            mWe.next    = True
            yield clk.posedge #TODO add delay for timing
            cState.next = tState.FETCH
        elif cState == tState.HALT:
            pass

    return logic
