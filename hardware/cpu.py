# -*- coding: utf-8 -*-
from myhdl import *


def cpu(clk, reset, addr,
        addrymux1, addrymux0, pmux,
        addrBuf, op2Buf, addr14Buf, ryBuf, aluBuf, pcBuf,
        enIr, enPc, enReg, enJump, enCall, enSup,
        enMRR, enMDR, enMAR, MRRbuf, MDRbuf, mWe, mOe):
    """
        This is a cpu state maschine. Let's see how far we come.
        All parameters are Signals as usual.

        clk       (Ibool) -- The clock
        reset     (Ireset)-- The reset signal
        addr      (I5)    -- Next action
        addrymux1 (Obool) -- mux1 for reginput
        addrymux0 (Obool) -- mux0 for reginput
        pmux      (Obool) -- if true, dx will be incremented by 4, decremented otherwise (used for push/pop)
        pcmux1    (Obool) -- pcMuxSelector
        pcmux0    (Obool) -- pcMuxSelector
        addrBuf   (Obool) -- bufbit for addr (pc+imm or reg)
        op2Buf    (Obool) -- bufbit for second opcode
        addr14Buf (Obool) -- bufbit for addr14buf
        ryBuf     (Obool) -- bufbit for content of y register
        aluBuf    (Obool) -- bufbit for alu
        pcBuf     (Obool) -- bufbit for pc (programcounter)
        enIr      (Obool) -- enable IR
        enPc      (Obool) -- enable ProgrammCounter
        enReg     (Obool) -- enable registe write
        enJump    (Obool) -- enable jumping
        enCall    (Obool) -- force jumping
        enSup     (Obool) -- enable statusUpdate
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

    def presetSignals():
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
        enPc.next = False
        enReg.next = False
        enSup.next = False
        enJump.next = False
        enCall.next = False
        enMRR.next = False
        enMDR.next = False
        enMAR.next = False
        MRRbuf.next = False
        MDRbuf.next = False
        mWe.next = False
        mOe.next = False

    def loadFromRam():
        """Takes the addr from the bus and puts the value from the memory to the bus"""
        enMAR.next = True
        yield clk.posedge
        presetSignals()
        mOe.next = True
        yield clk.posedge #TODO add delay for timing
        presetSignals()
        mOe.next = True
        enMRR.next = True
        yield clk.posedge
        presetSignals()
        MRRbuf.next = True

    def saveToRam():
        """Takes the value from the bus and takes it to the addr. MAR must have the addr already"""
        enMDR.next = True
        yield clk.posedge
        enMDR.next  = True
        yield clk.posedge
        presetSignals()
        MDRbuf.next = True
        mWe.next    = True
        yield clk.posedge #TODO add delay for timing

    @instance
    def logic():
        while True:
            yield clk.posedge, reset.posedge

            if reset == reset.posedge:
                presetSignals()
                state.next = tState.FETCH
                continue

            presetSignals() #this is important!

            if   state == tState.UNKNOWN: #TODO mir gefällt die Lösung mit dem unknown state nicht, mal gucken, ob ich das besser hinbekomme
                print "UNKOWN"
                if   addr[5:3] == 0b00:
                    state.next = tState.ALUOP
                elif addr[5:3] == 0b01:
                    state.next = tState.JUMP
                elif addr[5:2] == 0b100:
                    state.next = tState.LOAD
                elif addr[5:2] == 0b101:
                    state.next = tState.STORE
                elif addr[5:2] == 0b110:
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
                print "FETCH"
                pcBuf.next = True
                enMAR.next = True
                yield clk.posedge
                presetSignals()
                mOe.next = True
                yield clk.posedge #TODO add delay for timing
                presetSignals()
                mOe.next = True
                enMRR.next = True
                yield clk.posedge
                presetSignals()
                MRRbuf.next = True
                enIr.next = True
                state.next = tState.DECODE
            elif state == tState.DECODE:
                print "DECODE"
                enPc.next   = True
                state.next = tState.UNKNOWN
            elif state == tState.ALUOP:
                print "ALUOP"
                aluBuf.next = True
                enReg.next  = True
                enSup.next  = True
                state.next = tState.FETCH
            elif state == tState.JUMP:
                print "JUMP"
                enJump.next = True
                enPc.next = True
                state.next = tState.FETCH
            elif state == tState.LOAD:
                print "LOAD"
                addrBuf.next = True
                enMAR.next = True
                yield clk.posedge
                presetSignals()
                mOe.next = True
                yield clk.posedge #TODO add delay for timing
                presetSignals()
                mOe.next = True
                enMRR.next = True
                yield clk.posedge
                presetSignals()
                MRRbuf.next = True
                enReg.next = True
                state.next = tState.FETCH
            elif state == tState.STORE:
                print "STORE"
                addrymux0.next = True
                addrymux1.next = True
                ryBuf.next = True
                enMAR.next = True
                yield clk.posedge
                presetSignals()
                op2Buf.next = True #the actual value to bus
                enMDR.next = True
                yield clk.posedge
                enMDR.next  = True
                yield clk.posedge
                presetSignals()
                MDRbuf.next = True
                mWe.next    = True
                yield clk.posedge #TODO add delay for timing
                state.next = tState.FETCH
            elif state == tState.ADR:
                print "ADR"
                enReg.next = True
                addrBuf.next = True
                state.next = tState.FETCH
            elif state == tState.PUSH: #TODO Push pop is maybe incorrect
                print "PUSH"
                addrymux1.next = True #decrement $14 by four
                pmux.next = False #yep, false!
                enReg.next = True
                addr14Buf.next = True
                yield clk.posedge
                addrymux1.next = True #put $14 as addr to bus
                ryBuf.next = True
                enMAR.next = True
                yield clk.posedge
                presetSignals()
                op2Buf.next = True
                enMDR.next = True
                yield clk.posedge
                enMDR.next  = True
                yield clk.posedge
                presetSignals()
                MDRbuf.next = True
                mWe.next    = True
                yield clk.posedge #TODO add delay for timing
                state.next = tState.FETCH
            elif state == tState.POP:
                print "POP"
                addrymux0.next = True #put $14 to the bus
                addrymux1.next = True
                addr14Buf.next = True
                enMAR.next = True
                yield clk.posedge
                presetSignals()
                mOe.next = True
                yield clk.posedge #TODO add delay for timing
                presetSignals()
                mOe.next = True
                enMRR.next = True
                yield clk.posedge
                presetSignals()
                MRRbuf.next = True
                addrymux1.next = True
                pmux.next = True #increment $14 by 4
                enReg.next = True
                addr14Buf.next = True
                state.next = tState.FETCH
            elif state ==tState.CALL:
                print "CALL"
                pcBuf.next = True
                addrymux0.next = True
                enReg.next = True
                yield clk.posedge
                enCall.next = True
                enPc.next = True
                state.next = tState.FETCH
            elif state == tState.SWI:
                print "SWI"
                pass
            elif state == tState.HALT:
                print "HALT"
                pass
            else:
                assert False

    return logic
