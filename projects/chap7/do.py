#!/usr/bin/env python3

""" VM backend """

import sys
import os

C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GOTO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8


def getElements(cmd):
    """ returns the components of the current line command """
    components = list(filter(lambda s: s != ' ', cmd.split(' ')))
    if '//' in components:
        components = components[:components.find('//')]
    return components


class Parser(object):
    """ Handles the parsing of a single .vm file, and encapsulates access to
    the input code. It reads VM commands, parses them, and provides convenient
    access to their components. In addition, it removes all white space and
    comments. """

    def __init__(self, filename):
        self.file = open(filename, 'r')

    def hasMoreCommands(self):
        """ Are there more commands in the input """
        last_tell = self.file.tell()
        new_line = self.file.readline()
        if new_line:
            if not new_line.strip():
                if not self.hasMoreCommands():
                    return False
            self.file.seek(last_tell)
            return True
        return False

    def advance(self):
        """ Reads the next command from the input and makes it the current
        command. Should be called only if hasMoreCommands() is true.     
        Initially there is no current command. """
        
        current_line = self.file.readline().strip()
        if '//' in current_line:
            current_line = current_line[:current_line.find("//")].strip()

        if not current_line:
            if not self.hasMoreCommands():
                raise Exception('no more valid lines')
            self.advance()
            return

        self.current_line = current_line

    def commandType(self):
        """ Returns the type of the current VM command. C_ARITHMETIC is
        returned for all the arithmetic commands.
        
        Types:
            C_ARITHMETIC,
            C_PUSH, C_POP,
            C_LABEL, C_GOTO,
            C_IF,
            C_FUNCTION,
            C_RETURN,
            C_CAL
        """
        multi_arg = {'push':C_PUSH, 'pop':C_POP, 'return':C_RETURN, 'call':C_CALL,
        'label':C_LABEL, 'goto':C_GOTO, 'if-goto':C_IF, 'function':C_FUNCTION}
        single_arg = ('add','sub','neg','eq','gt','lt','and','or','not')

        cmd = self.current_line
        elm = getElements(cmd)

        for type in single_arg: # single argument instructions
            if elm == [type]:
                return C_ARITHMETIC

        for type in multi_arg: # multi argument instruction
            if elm[0] == type:
                return multi_arg[type]
        
        raise Exception('invalid command: '+repr(cmd))

class CodeWriter(object):
    """ Translates VM commands into Hack assembly code. """

    def __init__(self, filename):
        self.file = open(filename, 'w')
        self.basename = os.path.basename(filename.split('.')[0])
        self.lineCount = 0
        self.writeLine("@256","D=A","@SP","M=D",
    #            '@500','D=A','@LCL','M=D',
                # insert here the other bases to be set
                "@START","0;JMP")
        self.writeLine("(toDTrue)","\tD=-1","\t@R15","\tA=M","\t0;JMP",
                        "(toDFalse)","\tD=0","\t@R15","\tA=M","\t0;JMP")
        self.writeLine("(START)")

    def updateLineCount(self, command:str):
        """ Checks wheter an input command is a 'valid Assembly' or just
        pseudo-code/VM Translator function. """
        
        validLineTests = (
            lambda cmd: cmd.startswith('@'),
            lambda cmd: cmd[:2] in ('A=','D=','M=')
        )

        for test in validLineTests:
            if test[command]:
                self.lineCount += 1
                return self.lineCount
        return False

    def writeLine(self, *lines):
        """ writes line to file """
        
        for line in lines:
            lineIndex = self.updateLineCount(line)
            print(str(lineIndex)+':' if lineIndex else '','\t',line)
            self.file.write(line+'\n')
        self.file.write('\n')

    def setFileName(filename:str):
        """ Informs the code writer that the translation of a
        new VM file has started. """

    def writeArithmetic(self, segment:str):
        """ Writes the assembly code that is the translation of the given
        arithmetic command. """
        cmp = getElements(segment)

        toR13 = ('@SP','A=M','D=M','@R13','M=D')
        toR14 = ('@SP','A=M','D=M','@R14','M=D')
        dec = ('@SP','M=M-1')
        inc = ('@SP','M=M+1')

        addR14R13 = ('@R14','D=M','@R13','D=D+M')
        subR14R13 = ('@R14','D=M','@R13','D=D-M')
        orR14R13 = ('@R14','D=M','@R13','D=D|M')
        andR14R13 = ('@R14','D=M','@R13','D=D&M')
        eqR14R13 = ('@R14','D=M','@R13','D=D&M')
        gtR14R13 = ('@R14','D=M','@R13','D=D&M')
        ltR14R13 = ('@R14','D=M','@R13','D=D&M')
        toD = ('@SP','A=M','D=M')
        notD = ('D=!D',)
        negD = ('D=-D',)
        # A is SP-2 value and B is SP-1 value
        Cmps = {'eq':'JEQ', # eq => A==B
                'gt':'JGT', # gt => A>B
                'lt':'JLT'} # lt => A<B

        storeD = ('@SP','A=M','M=D')

        lines = ['// '+segment]
        
        if cmp[0] in ('add','sub','eq','gt','lt','and','or'): # 2 arg funcs
            lines += dec
            lines += toR13
            lines += dec
            lines += toR14

            if cmp[0] == 'add':
                lines += addR14R13
            elif cmp[0] == 'sub':
                lines += subR14R13
            elif cmp[0] == 'or':
                lines += orR14R13
            elif cmp[0] == 'and':
                lines += andR14R13
            elif cmp[0] in ('eq', 'gt', 'lt'):
                global lastLabel
                goto = 'goto'+str(lastLabel)
                
                gotoStruct = (
                    '@R13','M=D', # store D (result of A-B) at @R13
                    '@%s'%goto, 'D=A', '@R15', 'M=D', '', # store gotoN at @R15
                    '@R13','D=M', # get D at @R13 again... (sigh.)
                    '@toDTrue', 'D;%s'%Cmps[cmp[0]],
                    '@toDFalse', '0;JMP', ''
                )
                
                lines += subR14R13
                lines += gotoStruct

                lines += ['(%s)' % goto]
                lastLabel += 1
        elif cmp[0] in ('neg','not'):
            lines += dec
            lines += toD
            lines += negD if cmp[0] == 'neg' else notD

        lines += storeD
        lines += inc

        self.writeLine(*lines)

    def writePushPop(self, segment:str):
        """ Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP. """

        piles = {'local':'LCL', 'argument':'ARG', 'temp':'5',
                'that':'THAT','this':'THIS'}

        cmp = getElements(segment)
        pile = cmp[1]
        index = cmp[2]

        print(cmp)
        
        dec = ("@SP","M=M-1") # increment sp lines
        inc = ("@SP","M=M+1") # decrement sp lines
        getAdd = ["@%s"%piles[pile] if pile not in
        ('constant','pointer','static') else '',
                "D=M", "@%s"%index, "D=D+A"] # D=add of pile[index]
        pop = ('@R13','M=D', # store add at @R13
            '@SP','A=M','D=M', # store content of stack at D
            '@R13','A=M','M=D' # store content of D at add inside @R13
            ) # pop Memory[D] to @SP
        push = ('A=D','D=M','@SP','A=M','M=D') # push @SP to Memory[D]

        lines = ['// '+segment]

        if cmp[1] in ('pointer','temp'):
        # such  locations are the segment themselves
        ## rather than a pointer to segments
            getAdd[1] = 'D=A'
            
            if cmp[1] == 'pointer':
                # push/pop pointer 0 => @THIS
                # push/pop pointer 1 => @THAT
                getAdd[3] = '@0' # there's no index to be added to address
                if cmp[2] == '0':
                    getAdd[0] = '@THIS'
                elif cmp[2] == '1':
                    getAdd[0] = '@THAT'
                else:
                    raise Exception('invalid instruction: '+segment)
        if cmp[1] == 'static':
            getAdd = ('@%s.%s' % (self.basename, cmp[2]), 'D=A')

        if cmp[0] == 'pop':
            lines += dec # decrement sp
            lines += getAdd # store add of pile[index] at D
            lines += pop # pop Memory[D] to @SP
            
        if cmp[0] == 'push':
            if cmp[1] == 'constant':
                constant = ('@%s'%cmp[2],'D=A','@SP','A=M','M=D')
                lines += constant # write lines for constants
            else:
                lines += getAdd # store add of pile[index] at D
                lines += push
            lines += inc # increment sp

        self.writeLine(*lines)

    def Close(self):
        """ Closes the output file. """
        self.file.close()

lastLabel = 0

def main():
    parser = Parser(filename)
    codewriter = CodeWriter(filename.split('.')[0]+'.asm')

    while parser.hasMoreCommands():
        parser.advance()
        type = parser.commandType()
        print(parser.current_line, "\ntype:", type)
        if type in (C_PUSH, C_POP):
            codewriter.writePushPop(parser.current_line)
        elif type == C_ARITHMETIC:
            codewriter.writeArithmetic(parser.current_line)

if __name__ == '__main__':
    filename = 'BasicTest.vm'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    main()
