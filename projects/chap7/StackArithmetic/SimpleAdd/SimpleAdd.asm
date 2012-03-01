@256
D=A
@SP
M=D
@START
0;JMP

(toDTrue)
	D=-1
	@R15
	A=M
	0;JMP

(toDFalse)
	D=0
	@R15
	A=M
	0;JMP

(START)

// push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R14
D=M
@R13
D=D+M
@SP
A=M
M=D
@SP
M=M+1

