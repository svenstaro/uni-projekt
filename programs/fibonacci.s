jmp .start

;.globl fibonacci
fibonacci:
; $1 - unsigned int
cmp $1, #1
jle $15

; $1 - current
; $2 - last
; $3 - counter
sub $3, $1, #1
mov $1, #1
mov $2, #0

.fib_loop:
add $4, $1, $2
mov $2, $1
mov $1, $4
subs $3, $3, #1
jnz .fib_loop
ret


.start:
mov $1, #20
call fibonacci
; TODO: Print correct value.
rst $1 ; should be 6765
halt
