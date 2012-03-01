// observation: this program, besides book's warranty of no need of
//// negative numbers multiplication, is capable of doing it! :)
// this program multiplies two numbers
    @R2
    M=0
    @times
    M=0
    @R0
    D=M
    // now, negative numbers workaroud
    @NEGNUM
    0;JMP
(NOWBACK)
    @times
    D=M
    @R1
    D=D-M
    @END
    D;JGE

(LOOP) // sums R0 to result R1 times
    @R0
    D=M
    @R2
    M=D+M
    @times
    M=M+1
    
    @times
    D=M
    @R1
    D=D-M
    @LOOP
    D;JLT
(END)
    @END
    0;JMP

// Negative numbers workaround
(NEGNUM)
    @R1
    D=M
    @NOWBACK
    D;JGE // if R1 >= 0, no problems ahead: jump back

    @R0
    M=!M
    M=M+1
    @R1
    M=!M
    M=M+1
    @NOWBACK
    0;JMP


