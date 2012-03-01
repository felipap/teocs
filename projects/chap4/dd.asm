// Computes sum=1+...+100
    @1
    M=1 // count=1
    @sum // allocated at RAM[16]
    M=0
(LOOP)
    @i
    D=M
    @100
    D=D-A // if count=100...
    @END
    D;JGT // goto end
    @i
    D=M
    @sum
    M=D+M // sum=sum+count
    @i
    M=M+1 // count=count+!
    @LOOP
    0;JMP
(END) // infinite loop
    @END
    0;JMP
