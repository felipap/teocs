#!/usr/bin/env python3

""" Assembler implementation. """

import sys

A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

class Parser(object):
    """ encapsulates access to the input code. reads an assembly language command, parses it, and provides convenient access to the command's components (fields and symbols). In addition, removes all white space and comments.
    """

    # current command => self.current_line # current line => self.current_line

    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.symbols = dict()

    def hasMoreCommands(self):
        """ are there more commands in the input? 
        returns: bool
        """
        last_tell = self.file.tell()
        if self.file.readline():
            self.file.seek(last_tell)
            return True
        return False

    def advance(self):
        """ Reads the next command from the input and makes it the current
        command. Should be called only if hasMoreCommands() is true. Initially
        there is not current command.
        returns: None
        """
        current_line = self.file.readline().strip()
        if '//' in current_line:
            current_line = current_line[:current_line.find("//")].strip()

        if not current_line and self.hasMoreCommands():
            self.advance()
            return

        self.current_line = current_line


    def commandType(self):
        """ Returns type of the current command:
        => A_COMMAND for @Xxx where Xxx is symbol or decimal
        => C_COMMAND for dest=comp;jump
        => L_COMMAND for (Xxx) where Xxx is symbol (pseudo-command)
        """
        command = self.current_line
        if command.startswith('@'):
            return A_COMMAND
        if (command[0],command[-1]) == ('(',')'):
            return L_COMMAND
        return C_COMMAND 
        # C cmds are of the form dest(=?

    def symbol(self):
        """ Returns the symbol or decimal Xxx of the current command @Xxx or
        (Xxx). Should be called only when commandType() is A_COMMAND or
        L_COMMAND.
        """
        if self.current_line.startswith('@'):
            return self.current_line[1:]
        return self.current_line[1:-1]

    def dest(self):
        """ Returns the dest mnemonic in the current C-command (8
        possibilities). Should be called only when commandType() is C_COMMAND.
        """
        # dest mnemonics are always before equal signs
        command = self.current_line

        if not '=' in command: # no destiny
            return None
        # then, dest is everything before the '='
        return command[:command.find('=')]

    def comp(self):
        """ Returns the comp mnemonic in the current C-command (28
        possibilities). Should be called only when commandType() is C_COMMAND.
        """
        # always present, between possible dest and jump mnemonics
        command = self.current_line
        
        if '=' in command:
            command = command[command.find('=')+1:]
        if ';' in command:
            command = command[:command.find(';')]
        
        return command

    def jump(self):
        """ Returns the jump mnemonic in the current C-command (8
        possibilities). Should be called only when commandType() is C_COMMAND.
        """
        # always after semicolons
        command = self.current_line

        if not ';' in command: # no jump
            return None
        # then, jump is everything after the ';'
        return command[command.find(';')+1:]


class Code(object):
    """ Translates Hack assembly language mnemonics into binary code. """
    # Code methods are the only responsibles for detecting invalid instructions

    def dest(self, mnemonic):
        """ Returns the binary code of the dest mnemonic (3 bits). """
    
        dests = {'null':'000', 'M':'001', 'D':'010', 'MD':'011',
                'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'}

        if mnemonic is None:
            return dests['null']
        if mnemonic in dests:
            return dests[mnemonic]
        return False
     
    def comp(self, mnemonic):
        """ Returns the binary code of the comp mnemonic (7 bits). """

        comp = {'-D': '0001111', '-A': '0110011', '-M': '1110011', 'M+1':
        '1110111', 'D-A': '0010011', 'M-1': '1110010', 'D-M': '1010011', '1':
        '0111111', '0': '0101010', 'D+A': '0000010', 'A-1': '0110010', 'D+M':
        '1000010', 'A': '0110000', 'D': '0001100', 'D+1': '0011111', 'A+1':
        '0110111', 'M': '1110000', 'A-D': '0000111', 'D-1': '0001110', 'D|A':
        '0010101', 'M-D': '1000111', 'D|M': '1010101', '!A': '0110001', '!D':
        '0001101', '!M': '1110001', 'D&M': '1000000', '-1': '0111010', 'D&A':
        '0000000'}

        comp['1+M'] = comp['M+1']
        comp['A+D'] = comp['D+A']
        comp['M+D'] = comp['D+M']
        comp['A|D'] = comp['D|A']
        comp['M|D'] = comp['D|M']
        comp['A&D'] = comp['D&A']
        comp['M&D'] = comp['D&M']

        if mnemonic in comp:
            return comp[mnemonic]
        return False

    def jump(self, mnemonic):
        """ Returns the binary code of the jump mnemonic (3 bits). """

        jump = {'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011',
                'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}
        
        if mnemonic is None:
            return jump['null']
        if mnemonic in jump:
            return jump[mnemonic]
        return False

class SymbolTable(object):
    """ Keeps a correspondence between symbolic labels and numeric addresses """

    def Constructor(self):
        """ Creates a new empty symbol table. """
        self.symboltable = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
        'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7':
        7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14':
        14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576}

    def addEntry(self, symbol:str, address:int):
        """ Adds the pair (symbol, address) to the table. """
        self.symboltable[symbol] = address

    def contains(self, symbol:str) -> bool:
        """ Does the symbol table contain the given symbol? """
        
        try:
            self.symboltable[symbol]
            return True
        except:
            return False

    def GetAddress(self, symbol:str) -> int:
       """ Returns the address associated with the symbol. """
       return self.symboltable[symbol]

toaddress = lambda num: bin(int(num))[2:].zfill(15) # returns 15 bit version

def main():
    parser = Parser(filename)
    code = Code()
    table = SymbolTable()

    instruction_count = 0 # counts valid instructions for jumps
    next_free_memory = 16 # 
    table.Constructor()

    # THIS SCRIPT IS DEVIDED INTO TWO PHASES, AS DOCUMENTED IN THE BOOK CHAPTER
    # FIRST PHASE:
    # reads all lines, counts the valid instructions, ignores all but
    # L_COMMANDS and stores these into the memory, so that, in the next phase,
    # instructions can refer to goto labels which hadn't been read yet.
    while parser.hasMoreCommands():
        parser.advance()
        cmd_type = parser.commandType()
        
        if cmd_type == L_COMMAND:
        # (Xxx), pseudo commands
            symb = parser.symbol()
            value = instruction_count
            table.addEntry(symb, value)
            print("(%s), add: %s (%s)" % (symb,value,toaddress(value)))

        elif cmd_type in (A_COMMAND, C_COMMAND):
        # advance pc for real instructions
            instruction_count += 1

    # SECOND PHASE:
    # reads all lines, ignores L_COMMANDS and to the basic translation process.
    instruction_count = 0        
    parser.file.seek(0) # return to beginning
    while parser.hasMoreCommands():
        parser.advance()
        cmd_type = parser.commandType()        
        
        if cmd_type == A_COMMAND:
        # @Xxx
            print(instruction_count, parser.current_line, end=" => ")
            symb = parser.symbol() # selects decimal or symbol

            output.write('0')
            if symb.isdigit(): # is decimal (no need to get db content)
                print('0', toaddress(symb))
                output.write(toaddress(symb))
            else: # is symbol (need to get db content)
                if table.contains(symb): # already in db
                    print('0', toaddress(table.GetAddress(symb)))
                    output.write(toaddress(table.GetAddress(symb)))
                else: # not in db yet, add entry
                    table.addEntry(symb, next_free_memory)
                    print('0',toaddress(next_free_memory))
                    output.write(toaddress(table.GetAddress(symb)))
                    next_free_memory += 1
            output.write('\n')

        elif cmd_type == C_COMMAND:
        # dest=comp;jump
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()

            print(instruction_count, parser.current_line, end=" => ")
            print('111',code.comp(comp), code.dest(dest), code.jump(jump))
            output.write('111'+code.comp(comp)+code.dest(dest)+code.jump(jump)+'\n')

        if cmd_type in (A_COMMAND, C_COMMAND):
        # advance pc for real instructions
            instruction_count += 1

    print("All saved to file %s.hack." % filename.split('.')[0])
    output.close()

if __name__ == '__main__':
    filename = 'ado.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    output = open('%s.hack' % filename.split('.')[0],'w')
    main()
