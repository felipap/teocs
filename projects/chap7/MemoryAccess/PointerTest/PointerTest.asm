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

// push constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 0
@SP
M=M-1
@THIS
D=A
@0
@0
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop pointer 1
@SP
M=M-1
@THAT
D=A
@1
@0
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop this 2
@SP
M=M-1
@THIS
D=M
@2
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop that 6
@SP
M=M-1
@THAT
D=M
@6
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

// push pointer 0
@THIS
D=A
@0
@0
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push pointer 1
@THAT
D=A
@1
@0
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

// push this 2
@THIS
D=M
@2
D=D+A
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

// push that 6
@THAT
D=M
@6
D=D+A
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

