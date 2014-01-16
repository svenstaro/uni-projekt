ld $14, .sp
mov $1, $14
push #34
push #42
sub $2, $1, $14
pop $1
pop $1

mov $1, #0
.loop_beg:
    push $1
    ; TODO: Print correct value.
    rst $1
    add $1, $1, #1
    cmp $1, #16
    jgt .loop_end
    jmp .loop_beg

.loop_end:

.loopo_beg:
    pop $1
    ; TODO: Print correct value.
    rst $1
    subs $1, $1, #1
    jlt .loopo_end
    jmp .loopo_beg
.loopo_end:

halt

.sp:
    .word 0x80000100
