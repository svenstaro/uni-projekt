# -*- coding: utf-8 -*-
from ctypes import c_bool
from myhdl import *


def cpu(clk, addr, addrymux1, addrymux0, pmux,
        addrBuf, op2Buf, addr14Buf, ryBuf, aluBuf, pcBuf,
        enIr, enZ, enN, enC, enV, enPC, enReg, enJump, pcmux1, pcmux0,
        enMRR, enMDR, enMAR, MRRbuf, MDRbuf, mWe, mOe):
    """
        This is a cpu state maschine. Let's see how far we come.
        All parameters are Signals as usual.

        clk       (Ibool) -- The clock
        addr      (I5)    -- Next action
        addrymux1 (Obool) -- mux1 for reginput
        addrymux0 (Obool) -- mux0 for reginput
        pmux      (Obool) -- if true, dx will be incremented by 4, decremented otherwise (used for push/pop)
        addrBuf   (Obool) -- bufbit for addr (pc+imm or reg)
        op2Buf    (Obool) -- bufbit for second opcode
        addr14Buf (Obool) -- bufbit for addr14buf
        ryBuf     (Obool) -- bufbit for content of y register
        aluBuf    (Obool) -- bufbit for alu
        pcBuf     (Obool) -- bufbit for pc (programcounter)
        enIr      (Obool) -- enable IR
        enZ       (Obool) -- enable zero-register
        enN       (Obool) -- enable negative-register
        enC       (Obool) -- enable carry-register
        enV       (Obool) -- enable overflow register
        enPC      (Obool) -- enable ProgrammCounter
        enReg     (Obool) -- enable registe write
        enJump    (Obool) -- enables jumping
        pcmux1    (Obool) -- pcMuxSelector
        pcmux0    (Obool) -- pcMuxSelector
        enMRR     (Obool) -- enable MemoryReadRegister
        enMDR     (Obool) -- enable MemoryDataRegister
        enMAR     (Obool) -- enable MemoryAddressRegister
        MRRbuf    (Obool) -- bufbit MemoryReadRegister
        MDRbuf    (Obool) -- bufbit MemoryDataRegister
        mWe       (Obool) -- memoryWriteEnable
        mOe       (Obool) -- memoryOutputEnable
    """

    tState = enum('UNKNOWN', 'FETCH', 'DECODE', 'ALUOP', 'JUMP', 'LOAD', 'STORE', 'ADR', 'PUSH', 'POP', 'CALL', 'SWI', 'ILLEGAL', 'HALT')  # TODO add more
    state = Signal(tState.FETCH)

    def preset():
        addrymux1.next = False
        addrymux0.next = False
        pmux.next = False
        addrBuf.next = False
        op2Buf.next = False
        addr14Buf.next = False
        ryBuf.next = False
        aluBuf.next = False
        pcBuf.next = False
        enIr.next = False
        enZ.next = False
        enN.next = False
        enC.next = False
        enV.next = False
        enPC.next = False
        enReg.next = False
        enJump.next = False
        pcmux1.next = False
        pcmux0.next = False
        enMRR.next = False
        enMDR.next = False
        enMAR.next = False
        MRRbuf.next = False
        MDRbuf.next = False
        mWe.next = False
        mOe.next = False

    def load():
        """Takes the addr from the bus and puts the value from the memory to the bus"""
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

    def save():
        """Takes the value from the bus and takes it to the addr. MAR must have the addr already"""
        enMDR.next = True
        yield clk.posedge
        enMDR.next  = True
        yield clk.posedge
        preset()
        MDRbuf.next = True
        mWe.next    = True
        yield clk.posedge #TODO add delay for timing

    @always(clk.posedge)
    def logic():
        preset() #this is important!

        if   state == tState.UNKNOWN: #TODO mir gefällt die Lösung mit dem unknown state nicht, mal gucken, ob ich das besser hinbekomme
            if   addr[4:2] == 0b00:
                state.next = tState.ALUOP
            elif addr[4:2] == 0b01:
                state.next = tState.JUMP
            elif addr[4:1] == 0b100:
                state.next = tState.LOAD
            elif addr[4:1] == 0b101:
                state.next = tState.STORE
            elif addr[4:1] == 0b110:
                state.next = tState.ADR
            elif addr      == 0b11100:
                state.next = tState.PUSH
            elif addr      == 0b11101:
                state.next = tState.POP
            elif addr      == 0b11110:
                state.next = tState.CALL
            elif addr      == 0b11111:
                state.next = tState.SWI
            else:
                state.next = tState.ILLEGAL # TODO add more
        elif state == tState.FETCH:
            pcBuf.next = True
            load()
            enIr.next = True
            state.next = tState.DECODE
        elif state == tState.DECODE:
            enPC.next   = True
            state._next = tState.UNKNOWN
        elif state == tState.ALUOP:
            enZ.next = True
            enN.next = True
            enC.next = True
            enV.next = True
            aluBuf.next = True
            enReg.next  = True
            state.next = tState.FETCH
        elif state == tState.JUMP:
            enJump.next = True
            enPC.next = True
        elif state == tState.LOAD:
            addrBuf.next = True
            load()
            enReg.next = True
            state.next = tState.FETCH
        elif state == tState.STORE:
            addrymux0.next = True
            addrymux1.next = True
            ryBuf.next = True
            enMAR.next = True
            yield clk.posedge
            preset()
            op2Buf.next = True #the actual value to bus
            save()
            state.next = tState.FETCH
        elif state == tState.ADR:
            enReg.next = True
            addrBuf.next = True
        elif state == tState.PUSH:
            addrymux1.next = True #decrement $14 by four
            enReg.next = True
            pmux.next = False #yep, false!
            addrBuf.next = True
            yield clk.posedge
            addrymux0.next = True #put $14 as addr to bus
            addrymux1.next = True
            ryBuf.next = True
            enMAR.next = True
            yield clk.posedge
            preset()
            op2Buf.next = True
            save()
        elif state == tState.POP:
            addrymux0.next = True #put $14 to the bus
            addrymux1.next = True
            addrBuf.next = True
            load()
            addrymux1.next = True
            pmux.next = True #increment $14 by 4
            enReg.next = True
            addrBuf.next = True
            state.next = tState.FETCH
        elif state ==tState.CALL:
            pcBuf.next = True
            addrymux0.next = True
            enReg.next = True
            yield clk.posedge
            pcmux0.next = True
            pcmux1.next = True
            enPC.next = True
            state.next = tState.FETCH
        elif state == tState.SWI:
            pass
        elif state == tState.HALT:
            pass
        else:
            assert True == False

    return logic
