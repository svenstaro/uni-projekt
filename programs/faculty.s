jmp .start

;.globl faculty
faculty:
; $1 - unsigned int
movs $2, $1
mov $1, #1
jz $15
.fac_loop:
mul $1, $1, $2
subs $2, $2, #1
jnz .fac_loop
ret


.start:
mov $1, #6
call faculty
; TODO: Print correct value.
rst $1 ; should be 720
halt
