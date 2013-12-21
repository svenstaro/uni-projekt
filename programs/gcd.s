jmp .start

;.globl gcd
gcd:
; $1 - int
; $2 - int

; $1 < 0 => $1 = -$1
cmp $1, #0
jgt .gcd_cont1
not $1, $1
add $1, $1, #1


; $2 == 0 => ggt = $1
.gcd_cont1:
cmp $2, #0
jz $15

; $1 > $2 => ggt($2, $1)
cmp $1, $2
jle .gcd_cont2
mov $3, $1
mov $1, $2
mov $2, $3
jmp gcd

; ggt($1, $2) = ggt($1, $2-$1)
.gcd_cont2:
sub $2, $2, $1
jmp gcd

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
