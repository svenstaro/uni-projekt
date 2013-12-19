jmp .start

strlen:
; $1 - char*
add $4, $1, #1

.strlen_start:
ld $2, $1
add $1, $1, #1
lsrs $0, $2, #24
jnz .strlen_start

.strlen_end:
sub $1, $1, $4
ret

.helloWorld:
.asciiz Hello, World

.start:
adr $1, .helloWorld
call strlen
swi #1
halt
