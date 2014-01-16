jmp .start

;.globl ackermann
ackermann:
cmp $1, #0
jne .ack_1

add $1, $2, #1
ret

.ack_1:
cmp $2, #0
jne .ack_2

sub $1, $1, #1
mov $2, #1
jmp ackermann

.ack_2:
push $1
push $15

sub $2, $2, #1
call ackermann

mov $2, $1

pop $15
pop $1

sub $1, $1, #1
jmp ackermann


.sp:
.word 0x80001000

.start:
ld $14, .sp

mov $1, #3
mov $2, #6
call ackermann
; TODO: print correct output
rst $1 ; should be 509
halt
