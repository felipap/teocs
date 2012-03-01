@256
D=A
@SP
M=D
@START
0;JMP

(toDTrue)
	D=1
	@R15
	A=M
	0;JMP
(toDFalse)
	D=0
	@R15
	A=M
	0;JMP

(START)

// push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop static 8
@SP
M=M-1
@StaticTest.8
D=A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// pop static 3
@SP
M=M-1
@StaticTest.3
D=A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// pop static 1
@SP
M=M-1
@StaticTest.1
D=A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push static 3
@StaticTest.3
D=A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@StaticTest.1
D=A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub
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
D=D-M
@SP
A=M
M=D
@SP
M=M+1

// push static 8
@StaticTest.8
D=A
A=D
D=M
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

