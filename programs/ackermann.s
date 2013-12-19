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
st $1, $14
sub $14, $14, #4

st $15, $14
sub $14, $14, #4

sub $2, $2, #1
call ackermann

mov $2, $1

add $14, $14, #4
ld $15, $14

add $14, $14, #4
ld $1, $14
sub $1, $1, #1
jmp ackermann


.start:
mov $14, #0x7ffe
lsl $14, $14, #1

mov $1, #3
mov $2, #6
call ackermann
swi #1 ; should be 509
halt
