clk $1
swi #1
call test
halt

test:
    nop
    clk $2
    mov $1, $2
    swi #1
    ret
