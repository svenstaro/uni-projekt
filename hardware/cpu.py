# -*- coding: utf-8 -*-
from myhdl import *


def cpu(clk, reset, addr, readybit, rsrready, rstready,
        addrymux1, addrymux0, pmux,
        addrBuf, op2Buf, addr14Buf, ryBuf, aluBuf, pcBuf, clkBuf, butBuf, rsrBuf,
        enAlu, enIr, enPc, enReg, enJump, enCall, enSup, enLed, enRst,
        enMMU, mmuBuf):
    """
        This is a cpu state maschine. Let's see how far we come.
        All parameters are Signals as usual.

        clk       (Ibool) -- The clock
        reset     (Ireset)-- The reset signal
        addr      (I7)    -- Next action
        readybit  (Ibool) -- readybit from MMU
        rsrready  (Ibool) -- readybit from rsr
        rstready  (Ibool) -- readybit from rst
        addrymux1 (Obool) -- mux1 for reginput
        addrymux0 (Obool) -- mux0 for reginput
        pmux      (Obool) -- if true, dx will be incremented by 4, decremented otherwise (used for push/pop)
        addrBuf   (Obool) -- bufbit for addr (pc+imm or reg)
        op2Buf    (Obool) -- bufbit for second opcode
        addr14Buf (Obool) -- bufbit for addr14buf
        ryBuf     (Obool) -- bufbit for content of y register
        aluBuf    (Obool) -- bufbit for alu
        pcBuf     (Obool) -- bufbit for pc (programcounter)
        clkBuf    (Obool) -- bufbit for counter
        butBuf    (Obool) -- bufbit for the buttons
        rsrBuf    (Obool) -- bufbit for rs232 receiver
        enAlu     (Obool) -- enable ALU
        enIr      (Obool) -- enable IR
        enPc      (Obool) -- enable ProgrammCounter
        enReg     (Obool) -- enable registe write
        enJump    (Obool) -- enable jumping
        enCall    (Obool) -- force jumping
        enSup     (Obool) -- enable statusUpdate
        enLed     (Obool) -- enable Led
        enRst     (Obool) -- enable rs232 transmitter
        enMMU     (Obool) -- enable Memory managment unit
        mmuBuf    (Obool) -- bufbit for mmu
    """

    tState = enum('UNKNOWN', 'FETCH', 'DECODE', 'ALUOP', 'JUMP', 'LOAD', 'STORE',
                  'ADR', 'PUSH', 'POP', 'CALL', 'CLOCK', 'SWI', 'HWI', 'RSR', 'RST', 'HALT', 'ILLEGAL')
    state = Signal(tState.FETCH)
    substate = Signal(modbv(0)[4:])

    @always_seq(clk.posedge, reset=reset)
    def logic():
        ##### Presetting signals!
        addrymux1.next = False
        addrymux0.next = False
        pmux.next = False
        addrBuf.next = False
        op2Buf.next = False
        addr14Buf.next = False
        ryBuf.next = False
        aluBuf.next = False
        pcBuf.next = False
        clkBuf.next = False
        butBuf.next = False
        rsrBuf.next = False
        enAlu.next = False
        enIr.next = False
        enPc.next = False
        enReg.next = False
        enSup.next = False
        enJump.next = False
        enCall.next = False
        enLed.next = False
        enRst.next = False
        enMMU.next = False
        mmuBuf.next = False

        if __debug__:
            print state

        ##### UNKNOWN
        if   state == tState.UNKNOWN: # TODO mir gefällt die Lösung mit dem unknown state nicht, mal gucken, ob ich das besser hinbekomme
            if   addr[7:5] == 0b00:
                state.next  = tState.ALUOP
            elif addr[7:5] == 0b01:
                state.next  = tState.JUMP
            elif addr[7:4] == 0b100:
                state.next  = tState.LOAD
            elif addr[7:4] == 0b101:
                state.next  = tState.STORE
            elif addr[7:4] == 0b110:
                state.next  = tState.ADR
            elif addr[7:2] == 0b11100:
                state.next  = tState.PUSH
            elif addr[7:2] == 0b11101:
                state.next  = tState.POP
            elif addr[7:1] == 0b111100:
                state.next  = tState.CALL
            elif addr[7:1] == 0b111101:
                state.next  = tState.CLOCK
            elif addr[7:0] == 0b1111100:
                state.next  = tState.SWI
            elif addr[7:0] == 0b1111101:
                state.next  = tState.HWI
            elif addr[7:0] == 0b1111110:
                state.next  = tState.RSR
            elif addr[7:0] == 0b1111111:
                state.next  = tState.RST
            else:
                state.next  = tState.ILLEGAL # TODO add more

        ##### FETCHING
        elif state == tState.FETCH:
            if not readybit and substate == 0: #check if we can begin
                pass
            else:
                if substate == 0:
                    enMMU.next = True
                    pcBuf.next = True
                    substate.next = substate + 1
                elif substate == 1:
                    substate.next = substate + 1 # specification says, wait at least 1 cycle!
                elif not readybit:
                    pass
                elif readybit:
                    mmuBuf.next = True
                    enIr.next = True
                    substate.next = 0
                    state.next = tState.DECODE

        ##### DECODING
        elif state == tState.DECODE:
            enPc.next  = True
            state.next = tState.UNKNOWN

        ##### ALUOP
        elif state == tState.ALUOP:
            enAlu.next = True
            aluBuf.next = True
            enReg.next  = True
            enSup.next  = True
            state.next = tState.FETCH

        ##### JUMPING
        elif state == tState.JUMP:
            enJump.next = True
            enPc.next = True
            state.next = tState.FETCH

        ##### LOADING
        elif state == tState.LOAD:
            if not readybit and substate == 0: # check if we can begin
                pass
            else:
                if substate == 0:
                    enMMU.next = True
                    addrBuf.next = True
                    substate.next = substate + 1
                elif substate == 1:
                    substate.next = substate + 1 # specification says, wait at least 1 cycle!
                elif not readybit:
                    pass
                elif readybit:
                    mmuBuf.next = True
                    enReg.next = True
                    substate.next = 0
                    state.next = tState.FETCH

        ##### STORING DATA INTO RAM
        elif state == tState.STORE:
            if not readybit and substate == 0: # check if we can begin
                pass
            else:
                if substate == 0:
                    addrymux0.next = True
                    addrymux1.next = True
                    ryBuf.next = True
                    enMMU.next = True
                    substate.next = substate + 1
                elif substate == 1:
                    op2Buf.next = True # the actual value to bus
                    enMMU.next = True
                    substate.next = 0
                    state.next = tState.FETCH


        ##### ADRESS INSTR
        elif state == tState.ADR:
            enReg.next = True
            addrBuf.next = True
            state.next = tState.FETCH

        ##### PUSH
        elif state == tState.PUSH:
            if not readybit and substate == 0: # check if we can begin
                pass
            else:
                if substate == 0:
                    addrymux1.next = True # decrement $14 by four
                    pmux.next = False # yep, false!
                    enReg.next = True
                    addr14Buf.next = True
                    substate.next = substate + 1
                elif substate == 1:
                    addrymux1.next = True # put $14 to memaddr
                    ryBuf.next = True
                    enMMU.next = True
                    substate.next = substate + 1
                elif substate == 2:
                    op2Buf.next = True
                    enMMU.next = True
                    substate.next = 0
                    state.next = tState.FETCH

        ##### POP
        elif state == tState.POP:
            if not readybit and substate == 0: # check if we can begin
                pass
            else:
                if substate == 0:
                    addrymux1.next = True # put $14 to memaddr
                    ryBuf.next = True
                    enMMU.next = True
                    substate.next = substate + 1
                elif substate == 1: # while we wait, we increment $14 by 4
                    addrymux1.next = True
                    pmux.next = True
                    enReg.next = True
                    addr14Buf.next = True
                    substate.next = substate + 1
                elif not readybit:
                    pass
                elif readybit:
                    mmuBuf.next = True
                    addrymux1.next = True
                    addrymux0.next = True
                    enReg.next = True
                    substate.next = 0
                    state.next = tState.FETCH

        ##### CALL
        elif state == tState.CALL:
            substate.next = substate + 1
            if substate == 0:
                pcBuf.next = True
                addrymux0.next = True
                enReg.next = True
            elif substate == 1:
                enCall.next = True
                enPc.next = True
                substate.next = 0
                state.next = tState.FETCH

        ##### CLK
        elif state == tState.CLOCK:
            clkBuf.next = True
            addrymux0.next = True
            addrymux1.next = True
            enReg.next = True
            state.next = tState.FETCH

        ##### SWI
        elif state == tState.SWI:
            ryBuf.next = True
            state.next = tState.FETCH

        ##### HWI
        elif state == tState.HWI:
            #TODO
            pass

        ##### RSR
        elif state == tState.RSR:
            if rsrready:
                rsrBuf.next = True
                addrymux0.next = True
                addrymux1.next = True
                enReg.next = True
                state.next = tState.FETCH

        ##### RST
        elif state == tState.RST:
            enRst.next = True
            op2Buf.next = True

            if rstready:
                state.next = tState.FETCH

        ##### HALT
        elif state == tState.HALT:
            pass

        ##### ILLEGAL
        else:
            assert False

    return logic
