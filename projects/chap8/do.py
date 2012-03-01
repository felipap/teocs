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

TYPES = {
    C_ARITHMETIC:'C_ARITHMETIC',
    C_PUSH:'C_PUSH',
    C_POP:'C_POP',
    C_LABEL:'C_LABEL',
    C_GOTO:'C_GOTO',
    C_IF:'C_IF',
    C_FUNCTION:'C_FUNCTION',
    C_RETURN:'C_RETURN',
    C_CALL:'C_CALL',
}

CODE = {
	# Stack Pointer Arithmetics
	'dec': ('@SP', 'M=M-1'), # increments SP
	'inc': ('@SP', 'M=M+1'), # decrements SP

	# stores *(SP), to following memory
	'toR13': ('@SP', 'A=M', 'D=M', '@R13', 'M=D'),
	'toR14': ('@SP', 'A=M', 'D=M', '@R14', 'M=D'),
	'toD': ('@SP', 'A=M', 'D=M'),
	
	# executes functiionsons below and store at D
	## arguments: @R13 and @R14
	'addR14R13': ('@R14', 'D=M', '@R13', 'D=D+M'),
	'subR14R13': ('@R14', 'D=M', '@R13', 'D=D-M'),
	'orR14R13': ('@R14', 'D=M', '@R13', 'D=D|M'),
	'andR14R13': ('@R14', 'D=M', '@R13', 'D=D&M'),
	'eqR14R13': ('@R14', 'D=M', '@R13', 'D=D&M'),
	'gtR14R13': ('@R14', 'D=M', '@R13', 'D=D&M'),
	'ltR14R13': ('@R14', 'D=M', '@R13', 'D=D&M'),
	## arguments: D
	'notD': ('D=!D', ),
	'negD': ('D=-D', ),
	
	# push D to stack
	'storeD': ('@SP', 'A=M', 'M=D'),

	# A is SP-2 value and B is SP-1 value
	'Cmps': {'eq':'JEQ', # eq => A==B
	        'gt':'JGT', # gt => A>B
        	'lt':'JLT'}, # lt => A<B

	# push
	'push': ('A=D', 'D=M', '@SP', 'A=M', 'M=D'), # Mem[D] <- *SP
	# pop
	'pop': ('@R13', 'M=D', # R13 <- D (address)
            '@SP', 'A=M', 'D=M', # D <- *SP
            '@R13', 'A=M', 'M=D'), # *(R13) <- D
}

__usage__ = "usage: %s <file/folder>" % __file__

def get_elements(cmd):
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
        self.current_line = None

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
            C_LABEL, C_GOTO, # chapter 8 on
            C_IF,
            C_FUNCTION,
            C_RETURN,
            C_CALL
        """

        arithmetic = ('add', 'sub', 'and', 'or', 'not', 'eq', 'gt', 'lt', 'neg')

        tests = {
            C_PUSH: lambda elm: len(elm) == 3 and elm[0] == 'push',
            C_POP: lambda elm: len(elm) == 3 and elm[0] == 'pop',
            C_ARITHMETIC: lambda elm: len(elm) == 1 and elm[0] in arithmetic,
            C_LABEL: lambda elm: len(elm) == 2 and elm[0] == 'label',
            C_GOTO: lambda elm: len(elm) == 2 and elm[0] == 'goto',
            C_IF: lambda elm: len(elm) == 2 and elm[0] == 'if-goto',
            C_FUNCTION: lambda elm: len(elm) == 3 and elm[0] == 'function',
            C_RETURN: lambda elm: len(elm) == 1 and elm[0] == 'return',
            C_CALL: lambda elm: len(elm) == 3 and elm[0] == 'call'
        }
        
        elm = get_elements(self.current_line)

        for cmd_type in tests:
            if tests[cmd_type](elm):
                return cmd_type
        return None

class CodeWriter(object):
    """ Translates VM commands into Hack assembly code.
    
    class variables are explained below:
    self.parent:
        keeps information about the name of the current class in the assembly
        code. this is essencial for the usage of static variables.
    self.line_count:
        keeps track of the lines counting for the program. then, the user can
        access the assembly instruction by checking the correspondent line on
        the program standart output.
    self.goto_count:
        keeps track of the gotos required in arithmetic comparisons.
    self.label_count:
        keeps track of function calls count and allows the program to assign
        different labels to different return addresses (the fucking "BUG" that
        took me many nights to solve).
    self.current_function:
        defined just in case no function is entered in a single .vm file.
    """

    def __init__(self, filename):
        self.file = open(filename, 'w')
        self.parent = 'foo'
        self.current_function = 'bar'
        self.line_count = 0
        self.goto_count = 0
        self.label_count = dict()
        self.writeInit()

    def setParent(self, classname):
        """ sets current parent name """
        self.parent = classname 
        self.writeLine('// current class: %s' % self.parent)
    
    def close(self):
        """ closes the output file and ends the stream """
        self.file.close()

    def updateLineCount(self, command):
        """ Checks wheter an input command is a 'valid Assembly' or just
        pseudo-code/VM Translator function.
        """

        validLineTests = ( 
            lambda cmd: cmd.startswith('@'),
            lambda cmd: cmd[:2] in ('A=', 'D=', 'M='),
            lambda cmd: cmd[:3] in ('A;J', 'D;J', 'M;J', '0;J')
        )   

        for test in validLineTests:
            if test(command.strip()):
                self.line_count += 1
                return self.line_count
        return False

    def writeLine(self, *lines):
        """ writes lines to file """

        for line in lines:
            lineIndex = self.updateLineCount(line)
            print(str(lineIndex-1)+':' if lineIndex else '', '\t', line)
            self.file.write(line+'\n')
        self.file.write('\n')

    def writeInit(self):
        """ Writes assembly code that effects the VM initialization, also
        called *bootstrap code*. This code must be placed at the beginning of
        the output file.
        """
        
        self.writeLine("@256", "D=A", "@SP", "M=D") # set sp to 256
        self.writeLine(*self.writeCall("call Sys.init 0"))
        # set D = -1 (true)
        self.writeLine("(toDTrue)", "\tD=-1", "\t@R15", "\tA=M", "\t0;JMP")
        # set D = 0 (false)
        self.writeLine("(toDFalse)", "\tD=0", "\t@R15", "\tA=M", "\t0;JMP")

    def writeArithmetic(self, segment):
        """ Writes the assembly code that is the translation of the given
        arithmetic command.
        """

        # A is SP-2 value and B is SP-1 value
        Cmps = {'eq':'JEQ', # eq => A==B
                'gt':'JGT', # gt => A>B
                'lt':'JLT'} # lt => A<B

        twoarg_functions = ('add', 'sub', 'eq', 'gt', 'lt', 'and', 'or')
        onearg_functions = ('not', 'neg')

        comparison = get_elements(segment)
        print(comparison)
        lines = []
        lines.append('// '+segment)

        if comparison[0] in twoarg_functions:
            # LIFO store to R13 and R14 and --SP twice
            lines += CODE['dec']
            lines += CODE['toR13']
            lines += CODE['dec']
            lines += CODE['toR14']
            
            if comparison[0] == 'add':
                lines += CODE['addR14R13']
            elif comparison[0] == 'sub':
                lines += CODE['subR14R13']
            elif comparison[0] == 'or':
                lines += CODE['orR14R13']
            elif comparison[0] == 'and':
                lines += CODE['andR14R13']

            elif comparison[0] in ('eq', 'gt', 'lt'):
                goto = ' % s.goto%s' % (self.current_function, self.goto_count)
                gotoStruct = (
                    '@R13', 'M=D', # store D (result of A-B) at @R13
                    '@%s' % goto, 'D=A', '@R15', 'M=D', '', # R15 <= gotoN
                    '@R13', 'D=M', # get D back at @R13 again... (*sigh*)
                    '@toDTrue', 'D;%s' % Cmps[comparison[0]], # D true if cond
                    '@toDFalse', '0;JMP' # set D false
                )
                
                lines += CODE['subR14R13']
                lines += gotoStruct

                lines += ['(%s)' % goto]
                self.goto_count += 1
        elif comparison[0] in onearg_functions: # neg or not
            # LIFO store to D and --SP
            lines += CODE['dec']
            lines += CODE['toD']
            if comparison[0] == 'neg':
                lines += CODE['negD']
            elif comparison[0] == 'not':
                lines += CODE['notD']
        
        # push D to stack (and increment)
        lines += CODE['storeD']
        lines += CODE['inc']

        return lines

    def writePushPop(self, segment):
        """ Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP. """

        def getAddress(pile, index):
            """ stores memory address of <pile> <index> at D """
            piles = {'local':'LCL', 'argument':'ARG', 'temp':'5',
                    'that':'THAT', 'this':'THIS', 'pointer':'WHATEVER'}
            return ["@%s" % piles[pile], "D=M", "@%s" % index, "D=D+A"]
        
        comparison = get_elements(segment)
        print(comparison)
        pile, index = comparison[1:]

        constant = ('@%s' % index, 'D=A', '@SP', 'A=M', 'M=D')
        
        # processes the absolute address of pile[index] at memory
        getAdd = ''
        if pile not in ('constant', 'static'):
            getAdd = getAddress(pile, index)
        
        lines = []
        lines.append('// '+segment)

        # locations above are the segments themselves
        ## not pointers to them
        if comparison[1] in ('pointer', 'temp'):
            getAdd[1] = 'D=A'
        
        # push/pop pointer 0 => @THIS
        # push/pop pointer 1 => @THAT
        if comparison[1] == 'pointer':
            getAdd[3] = '@0' # there's no index to be added to address
            getAdd[0] = '@THIS' if index == '0' else '@THAT'
            assert index in '01', 'invalid instruction: '+segment

        # files mapping
        # IMPLEMENTATION NEEDED
        if comparison[1] == 'static':
            getAdd = ('@%s$%s' % (self.parent, comparison[2]), 'D=A')
        
        if comparison[0] == 'pop':
            lines += CODE['dec']
            lines += getAdd
            lines += CODE['pop']
          
        if comparison[0] == 'push':
            if pile == 'constant':
                lines += constant
            else:
                lines += getAdd
                lines += CODE['push']
            lines += CODE['inc']
        return lines

    def writeLabel(self, segment):
        """ Writes assembly code that effects the label command. """

        cmd = get_elements(segment)
        lines = []
        lines.append('// '+segment)
        lines += ['(%s$%s)' % (self.current_function, cmd[1])]
        return lines
    
    def writeGoto(self, segment):
        """ Writes assembly code that effects the goto command. """

        cmd = get_elements(segment) 
        
        lines = []
        lines += ['// '+segment]
        lines += ["@%s$%s" % (self.current_function, cmd[1])]
        lines += ["0;JMP"]

        return lines

    def writeIfGoto(self, segment):
        """ Writes assembly code that effects the if-goto command. """

        cmd = get_elements(segment)
        lines = []
        lines += ['// '+segment]
        lines += ['@SP', 'M=M-1', 'A=M', 'D=M']
        lines += ['@%s$%s' % (self.current_function, cmd[1])]
        lines += ['D;JNE']

        return lines

    def writeFunction(self, segment):
        """ Writes assembly code that effects the function command.
        Process: 'function f k'
        // declare function f that has k local variables
            (f) // declare label for function entry
                repeat k times: // k = number of local variables
                    push 0 // initialize them all to 0
        """
        
        cmd = get_elements(segment)
        name, nlocals = cmd[1:]
        self.current_function = name

        lines = []
        lines += ['// '+segment]
        lines += ['(%s)' % name]
        lines += ['@%s' % nlocals, 'D=A', '@R13', 'M=D'] # store locals num
        lines += ['(%s._func_storage_start)' % name,
                    '@%s._func_storage_end' % name,
                        'D;JLE', # skip if D <= 0
                    '@SP', 'M=M+1', # increment SP
                    'D=D-1', # decrement index (stored at D)
                    '@SP', 'A=M', 'M=0', # set cell to 0
                    '@%s._func_storage_start' % name, '0;JMP', # jump back
                '(%s._func_storage_end)' % name,
        ]
        lines += ['@0']*20 # add this for easier debugging
        
        return lines

    def writeCall(self, segment):
        """ Writes assembly code that effects the call command.
        Process: 'call f n'
        // calling function f with k arguments
            push return-address // (using label declared below)
            push LCL // save LCL of the calling function
            push ARG // save ARG of the calling function
            push THIS // save ARG of the calling function
            push THAT // save ARG of the calling function
            ARG = SP-n-5 // reposition ARG (n=num of args)
            LCL = SP // reposition LCL
            goto f // transfer control
        (return address) // declare label for return-address
        """

        cmd = get_elements(segment)
        function, args = cmd[1:]
        
        if not function in self.label_count:
            self.label_count[function] = 1
        else:
            self.label_count[function] += 1
        
        label = ' % s.return%s' % (function, self.label_count[function])

        lines = []
        lines += ['// '+segment]
        lines += ['@'+label, 'D=A',
                    '@SP', 'A=M', 'M=D',
                    '@SP', 'M=M+1']
        lines += ['@LCL', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
        lines += ['@ARG', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
        lines += ['@THIS', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
        lines += ['@THAT', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
        lines += ['@SP', 'D=M', '@%s' % args, 'D=D-A', '@5',
                                                'D=D-A', '@ARG', 'M=D']
        lines += ['@SP', 'D=M', '@LCL', 'M=D']
        lines += ['@%s' % function, '0;JMP']
        lines += ['(%s)' % label]
        
        return lines
    
    def writeReturn(self, segment):
        """ Writes code that effects the return command.
        Process: 'return'
        // inside a function
            FRAME = LCL // FRAME is a temporary variable
            RET = *(FRAME-5) // put return-add in a temp. var.
            *ARG = pop() // reposition the return value for the caller
                    // aka pop the stack topmost element to the add inside ARG
            SP = ARG+1 // restore SP of the caller
            THAT = *(FRAME-1) // restore THAT of the caller
            THIS = *(FRAME-2) // restore THIS of the caller
            ARG = *(FRAME-3) // restore ARG of the caller
            LCL = *(FRAME-4) // restore LCL of the caller
            goto RET // goto return-add (in the caller's code)
        """

        lines = []
        lines += ['// %s' % segment]
        lines += ['/// R5 <= LCL', '@LCL', 'D=M', '@R5', 'M=D'] # R5 => FRAME
        lines += ['/// R6 <= caller return add',
                    '@R5', 'D=M', '@5', 'D=D-A', 'A=D', 'D=M', # D = *(FRAME-5)
                    '@R6', 'M=D'] # R6 => caller's return-address
        
        lines += ['/// store pop at add inside ARGs',
                    '@SP', 'M=M-1',
                    'A=M', 'D=M', # D => topmost stack element
                    '@ARG', 'A=M', 'M=D'] # store D at ARG's add
        
        lines += ['/// SP = ARG+1', '@ARG', 'D=M', '@SP', 'M=D+1']
        lines += ['/// restore THAT', '@R5', 'D=M',
                    '@1', 'A=D-A', 'D=M', 'M=1', '@THAT', 'M=D'] # restore THAT
        lines += ['/// restore THIS', '@R5', 'D=M',
                    '@2', 'A=D-A', 'D=M', 'M=1', '@THIS', 'M=D'] # restore THIS
        lines += ['/// restore ARG', '@R5', 'D=M',
                    '@3', 'A=D-A', 'D=M', 'M=1', '@ARG', 'M=D'] # restore ARG
        lines += ['/// restore LCL', '@R5', 'D=M',
                    '@4', 'A=D-A', 'D=M', 'M=1', '@LCL', 'M=D'] # restore LCL
        lines += ['/// jump to caller._return', '@R6', 'A=M', '0;JMP']

        return lines

    def Close(self):
        """ Closes the output file. """
        self.file.close()

getBasename = lambda filename: os.path.basename(os.path.splitext(filename)[0])

def work_many(files):
    """ function does the work for files in a folder translation """

    for file in files:
        codewriter.setParent(getBasename(file))
        work_file(file)

def work_file(filename):
    """ functions does the work for a single file translation """

    parser = Parser(filename)
    while parser.hasMoreCommands():
        parser.advance()
        cmd_type = parser.commandType()

        if cmd_type is None:
            raise Exception('invalid command: '+repr(parser.current_line))
        
        print('-' * 40)
        print(repr(parser.current_line), "\ntype:", TYPES[cmd_type])
       
        functions = {
            C_PUSH: codewriter.writePushPop,
            C_POP: codewriter.writePushPop,
            C_ARITHMETIC: codewriter.writeArithmetic,
            C_LABEL: codewriter.writeLabel,
            C_IF: codewriter.writeIfGoto,
            C_GOTO: codewriter.writeGoto,
            C_FUNCTION: codewriter.writeFunction,
            C_CALL: codewriter.writeCall,
            C_RETURN: codewriter.writeReturn
        }
        
        if cmd_type in functions:
            codewriter.writeLine(*functions[cmd_type](parser.current_line))

isfile = os.path.isfile
isdir = os.path.isdir

def main():
    """ main function, dahh 
    manages the files and output file and stuff."""
    global codewriter 
    if os.path.isfile(sys.argv[1]):
        inputfile = sys.argv[1]
        print("input file: %s" % inputfile) 

        codewriter = CodeWriter(getBasename(inputfile)+'.asm')
        work_file(inputfile)
        
        print("all written to %s" % inputfile)
    elif os.path.isdir(sys.argv[1]):
        folder = os.path.abspath(sys.argv[1])
        print("input folder: %s" % folder)
        
        codewriter = CodeWriter(os.path.join(folder,
                                os.path.split(folder)[1]+'.asm'))
        filesBasename = filter(lambda file: file.endswith('.vm'),
                                        os.listdir(folder))
        files = list(map(lambda name: os.path.join(folder, name),
                                filesBasename))
        print(".vm files on folder: %s" % files)
        work_many(files)

        print("all written to %s" % (folder+".asm"))
    else:
        print("invalid file/folder address.", __usage__)
        exit()
    codewriter.close()

if __name__ == '__main__':
    isfile = os.path.isfile
    isdir = os.path.isdir
    
    if len(sys.argv) <= 1:
        print(__usage__)
        exit()
    main()
