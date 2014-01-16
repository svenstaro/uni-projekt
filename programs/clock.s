clk $1
; TODO: Print correct value.
rst $1
call test
halt

test:
    nop
    clk $2
    mov $1, $2
    ; TODO: Print correct value.
    rst $1
    ret
