jmp .start

;.globl gcd
gcd:
; Binary GCD
; $1 - x
; $2 - y
; ---
; $3 - cf2
; $4 - tmp

; Ensure $1 > $2
subs $4, $1, $2
jgt .gcd_cont1
add $2, $2, $4
sub $1, $2, $4

.gcd_cont1:
; If $2 == 0 then $1 is the result
tst $2, $2
jz $15

orr $4, $1, $2
mov $3, #0

; $1 >>= ctz($1|$2)
; $2 >>= ctz($1|$2)
.gcd_loop1:
rors $4, $4, #1
jlt .gcd_loop1_end
add $3, $3, #1
jmp .gcd_loop1

.gcd_loop1_end:
asr $1, $1, $3
asr $2, $2, $3



; $1 >>= ctz($1)
.gcd_loop2:
tst $1, #1
jnz .gcd_loop2_end
asr $1, $1, #1
jmp .gcd_loop2

.gcd_loop2_end:
.gcd_mainloop:

; $2 >>= ctz($2)
.gcd_mainloop_l:
tst $2, #1
jnz .gcd_mainloop_l_end
asr $2, $2, #1
jmp .gcd_mainloop_l

.gcd_mainloop_l_end:
; $1 == $2 => $1 is the result
; $1 < $2 => $1, $2 = $2, $1
; $2 = $2 - $1
subs $2, $2, $1
jeq .gcd_end
jgt .gcd_mainloop
add $1, $1, $2
sub $2, $0, $2
jmp .gcd_mainloop

.gcd_end:
lsl $1, $1, $3
ret

.a:
.word 150
.b:
.word 26

.start:
ld $1, .a
ld $2, .b
call gcd
swi #1 ; should be 2
halt
