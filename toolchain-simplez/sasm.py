#!/usr/bin/python3
# ------------------------------------------------------------------------------
# --  Asembler for the Simplez microprocessor
# --  (C) BQ November 2015. Written by Juan Gonzalez (obijuan)
# --  Python 3
# --  v1.2
# ------------------------------------------------------------------------------
# -- Released under the GPL v3 License
# ------------------------------------------------------------------------------
# - Grammar definition
# -
# --- A program is a list of lines with the END keyword in the end
#     (finished by EOL)
# --- Notice that after the END there could be more instructions, but
#     they will be ignored
# <program> ::= <lines> "END" EOL
#
# --- There could be more than one lines. Each line should be end by EOL
# <lines> ::= (<line> EOL+ )* | <lines>
#
# -- Each line can be a comment, a line of code followed by a commnet
# -- or just a simple line of code
# <line> ::= COMMENT | <lineofcode> COMMENT | <lineofcode>
#
# -- Lines of code can be either a directive or line with a simplez instructions
# <lineofcode> ::= <directive> | <lineinstruction>
#
# -- All the instruction can have a label in the beginning of the line
#   (optionally)
# <lineinstruction> ::= <instruction> | LABEL <instruction>
#
# -- There are 9 different simplez-F instructions
# <instruction> ::= <instLD>  | <insST>   | <instADD>  | <instBR> | <instBZ> |
# ----------------- <instCLR> | <instDEC> | <instHALT> | <instWAIT>
#

# - There are 4 different directives
# <directive> ::= <dirORG> | <dirEQU> | <dirRES> | <dirDATA>
#
# - ORG directive do not have any label in the left
#   The argument can be a number or a label
# - label (defined by the EQU directive)
# <dirORG> ::= ORG NUMBER | ORG LABEL
#
# -- EQU Directive
# <dirEQU> ::= LABEL EQU NUMBER
#
# -- DATA directive.  Label is optional
# <dirDATA> ::= LABEL DATA <datacollection> |  DATA <datacollection>
#
# -- Collection of data,separated by ,
# <datacollection> ::= <data> (,<data>)*
#
# -- Type of data accepted as "DATA"
# <data> ::= STRING | NUMBER
#
# -- RES directive. Label is optional
# <dirRES> ::= LABEL RES NUMBER | RES NUMBER
#

# -- Instruction LD
# <instLD> ::= LD <addr>
#
# -- The address can be giben numerically (eg. /501), or by label (eg. /ini)
# <addr> ::= ADDRNUM | ADDRLABEL
#
# -- Instruction ST
# <instST> ::= ST <addr>
#
# -- Instruction ADD
# <instADD> ::= ADD <addr>
#
# -- Instruction BR
# <instBR> ::= BR <addr>
#
# -- Instruction BZ
# <instrBZ> ::= BZ <addr>
#
# -- Instruction CLR
# <instrCLR> ::= CLR
#
# -- Instruction DEC
# <instrDEC> ::= DEC
#
# -- Istruction HALT
# <instrHAL> ::= HALT
#
# -- Instruction WAIT
# <instWAIT> ::= WAIT

# - Tokens:
#
# - EOL, EOF, COMMENT, LABEL, ORG, NUMBER, STRING, ADDRNUM, ADDRLABEL
# - LD, ST, ADD, BR, BZ, CLR, DEC, HALT, WAIT

# - COMMENT: ;(any ascii char)*
# - LABEL: (any ascii char)*  That is NOT a reserved word
# - NUMBER: Decimal or hexadecimal number:  [0-9]* | H'[0-9,a-f,A-F]*
# - STRING: "(any ascii char)"
# - ADDRNUM: /NUMBER
# - ADDRLABEL: /LABEL

import sys
import re

# --- Token types
(EOL, EOF, COMMENT, LABEL, ORG, NUMBER, ADDR,
 LD, ST, ADD, BR, BZ, CLR, DEC, HALT, WAIT, UNKNOWN, END, EQU, RES,
 DATA, STRING, COMMA) = (
 'EOL', 'EOF', 'COMMENT', 'LABEL', 'ORG', 'NUMBER',  'ADDR',
 'LD', 'ST', 'ADD', 'BR', 'BZ', 'CLR', 'DEC', 'HALT', 'WAIT', 'UNKNOWN', 'END',
 'EQU', 'RES', 'DATA', 'STRING', 'COMMA'
)

# -- default output file with the machine code for SIMPLEZ
OUTPUT_FILE = "prog.list"

VERSION = "v1.2"

# -- Instruction opcodes
OPCODES = {ST: 0, LD: 1, ADD: 2, BR: 3, BZ: 4,
           CLR: 5, DEC: 6, HALT: 7, WAIT: 0xF, DATA: 0xFF, }


class Token(object):
    """Token generator"""

    def __init__(self, type, value, line=None):
        self.type = type
        self.value = value
        self.line = line

    def __str__(self):

        # -- Print the Token line number
        string = "[{}] Token: ".format(self.line)

        # -- Case 1: These token have no value
        if self.type in [EOL, EOF, END, ORG, EQU, RES, DATA,
                         COMMA, LD, ST, ADD, BR, BZ, CLR, DEC, HALT, WAIT]:
            string += self.type

        # -- Case 2: These tokens have values
        elif self.type in [COMMENT, STRING, NUMBER, LABEL, ADDR]:
            string += "{} ({})".format(self.type, self.value)

        else:
            string += "Unknown ({})".format(self.value)

        return string

# ------------- Regular expresion definitions for the Lexer --------
# -- Decimal number
REGEX_DEC = r"[0-9]+"

# -- Hexadecimal number
REGEX_HEX = r"H\'[0-9a-fA-F]+"

# -- Comment
REGEX_COMMENT = r";[^\n]*"

# -- White spaces. \n is not included
REGEX_WSPACE = r"[ \t\r\f\v]+"

# -- Label
REGEX_LABEL = r"[a-zA-Z0-9_]+"

# -- String
REGEX_STRING = r"\"[^\"]*\""

# -- Numeric address (in decimal)
REGEX_ADDRNUM1 = r"/[0-9]+"

# -- Numeric address (in hexadecimal)
REGEX_ADDRNUM2 = r"/H\'[0-9a-fA-F]+"

# -- Address label
REGEX_ADDRLABEL = r"/[a-zA-Z0-9_]+"


class Lexer(object):
    """Lexical analyzer"""

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1

    def reset(self):
        self.pos = 0
        self.line = 1

    def check_hexnumber(self):
        """Check if it is an hexadecimal number. If so, return its value,
           else None
        """
        scan = re.match(REGEX_HEX, self.text[self.pos:].upper())
        if scan:
            self.pos += len(scan.group())

            # -- Return the number
            return int(scan.group()[2:], 16)
        else:
            return None

    def check_decimal(self):
        """Check if it is a decimal number. If so, return it svalue,
           else None"""

        scan = re.match(REGEX_DEC, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())
            return int(scan.group())

    def check_comment(self):
        """Check if it is a comment. It returns the comment or None"""

        scan = re.match(REGEX_COMMENT, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())
            return scan.group()[1:]

    def check_addr(self):
        """Check if it is an address"""

        # -- Case 1: Address in decimal
        scan = re.match(REGEX_ADDRNUM1, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())
            return int(scan.group()[1:])

        # -- Case 2: Address in hexadecimal
        scan = re.match(REGEX_ADDRNUM2, self.text[self.pos:].upper())
        if scan:
            self.pos += len(scan.group())
            return int(scan.group()[3:], 16)

        # -- Case 3: Address is a label
        scan = re.match(REGEX_ADDRLABEL, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())
            return scan.group()[1:]

    def check_directive(self):
        """Check if it is a directive"""

        for direct in [END, ORG, EQU, RES, DATA]:
            scan = re.match(direct+"\s", self.text[self.pos:].upper())
            if scan:
                self.pos += len(scan.group()[:-1])
                return direct

    def check_instruction(self):
        """Check if it is an instruction"""

        for instr in [LD, ST, ADD, BR, BZ, CLR, DEC, HALT, WAIT]:
            scan = re.match(instr+"\s", self.text[self.pos:].upper())
            if scan:
                self.pos += len(scan.group()[:-1])
                return instr

    def check_label(self):
        """Check if it is a label"""

        scan = re.match(REGEX_LABEL, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())
            return scan.group()

    def check_string(self):
        """Check if it is a string"""
        scan = re.match(REGEX_STRING, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())
            return scan.group()[1:-1]

    def get_token(self):
        """Get the next token from tex"""

        # -- Remove the white spaces (except \n)
        scan = re.match(REGEX_WSPACE, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())

        # -- Is it a commnet?
        comment = self.check_comment()
        if comment:
            return Token(COMMENT, comment, line=self.line)

        # -- Is it a hexadecimal number?
        hexnumber = self.check_hexnumber()
        if hexnumber is not None:
            return Token(NUMBER, hexnumber, line=self.line)

        # -- Is it a decimal number?
        number = self.check_decimal()
        if number is not None:
            return Token(NUMBER, number, line=self.line)

        # -- Is it a string?
        string = self.check_string()
        if string is not None:
            return Token(STRING, string, line=self.line)

        # -- Is it an address?
        addr = self.check_addr()
        if addr is not None:
            return Token(ADDR, addr, line=self.line)

        # -- Check if it is a directive
        direct = self.check_directive()
        if direct:
            return Token(direct, None, line=self.line)

        # -- Check if it is an instruction
        instr = self.check_instruction()
        if instr:
            return Token(instr, None, line=self.line)

        # -- Check if it is a label
        label = self.check_label()
        if label:
            return Token(LABEL, label, line=self.line)

        # --Get the current char
        try:
            current_char = self.text[self.pos]
        except IndexError:
            return Token(EOF, None, line=self.line)

        # -- Is it a EOL?
        if current_char == '\n':
            self.pos += 1
            line = self.line
            self.line += 1
            return Token(EOL, None, line=line)

        # -- Is it a COMMA?
        if current_char == ',':
            self.pos += 1
            return Token(COMMA, None, line=self.line)

        self.pos += 1
        return Token(UNKNOWN, current_char, line=self.line)

    def test(self):
        """Test the lexer"""

        string = ""
        while True:
            token = self.get_token()
            string += "{}\n".format(token)
            if token.type == EOF:
                return string


# ---------------------- AST
class Prog_AST(object):
    def __init__(self):
        self.addr = 0   # -- Current address
        self.linst = []  # -- List of instructions

        # -- Symbol table. It is used for storing the pairs label - address
        self.symtable = {}

    def add(self, inst):
        """Add the instruction in the current address.
           Increment the address counter
        """

        # -- Assign the current address
        inst.addr = self.addr

        # -- Insert the instruction
        self.linst.append(inst)

        # -- Increment the current address
        self.addr += 1

    def solve_labels(self):
        """semantic analysis. Assign a value to the instruction arguments
           that do not have a numeric value"""

        for instr in self.linst:

            # -- Check only the instructions with arguments
            if instr.arg is not None:
                # -- Check if the argument is a string
                if type(instr.arg) is str:
                    # -- It is a label. Put the label in the label attribute
                    instr.label = instr.arg

                    # -- Get the label's value from the symtable
                    try:
                        value = self.symtable[instr.label]
                    except KeyError:
                        raise Exception(
                            "Error: Line: {}: Symbol not defined: {}".format(
                                instr.line,
                                instr.label))

                    # -- Write the value in the argument
                    instr.arg = int(value)

    def assembly(self):
        """Write the program in assembly language"""
        string = ""
        addr = 0
        for instr in self.linst:
            # -- There is a gap between in the addresses
            if addr != instr.addr:
                string += "\n      ORG 0x{0:03X}\n".format(instr.addr)
                addr = instr.addr

            string += "{}\n".format(instr)
            addr += 1

        return string

    def size(self):
        """Calculate the program size (code, data), in words
         """

        # -- Calculate the size of data
        # -- Data above the address 504 is not counted
        sdata = 0
        scode = 0
        for instr in self.linst:
            # -- Only the data / code below 504 counts
            if instr.addr < 504:
                if instr.nemonic == DATA:
                    sdata += 1
                else:
                    scode += 1

        return scode, sdata

    def show_symbols(self):
        """Print the symbol table"""

        for key, value in self.symtable.items():
            print("{} = {}".format(key, value))

    def machine_code(self, asm=False):
        """Write the program in machine code"""
        string = ""
        if asm:
            string += "//mcode    addr nemonic\n"
            string += "//-----    ---- -------\n"

        addr = 0
        for instr in self.linst:
            if addr != instr.addr:

                if asm:
                    string += "\n"
                string += "@{0:03X}".format(instr.addr)
                if asm:
                    string += "  //--       ORG {0:03X}".format(instr.addr)

                string += "\n"
                addr = instr.addr

            string += "{:03X}".format(instr.mcode())
            if asm:
                string += "   //-- {}".format(instr)
            string += "\n"
            addr += 1

        return string


class Instruction(object):
    """Simplez instruction class"""

    def __init__(self, nemonic, arg=None, line=None):
        self.nemonic = nemonic  # -- Instruction name
        self.arg = arg          # -- Instruction argument
        self.line = line        # -- src line number where the inst. is located
        self.addr = None        # -- Address were the instruction is stored
        self.label = None       # -- If the argument is a label

    def opcode(self):
        """Return the instruction opcode"""
        return OPCODES[self.nemonic]

    def mcode(self):
        """Return the machine code"""
        if self.nemonic == "DATA":
            return self.arg
        elif self.nemonic == "WAIT":
            return 0xF00
        elif self.arg is not None:
            return (self.opcode() << 9) + self.arg
        else:
            return (self.opcode() << 9)

    def __str__(self):
        string = ""

        if self.addr is not None:
            string += "[{:03X}] ".format(self.addr)

        # -- Uncomment for showing the src line numbers
        # if self.line is not None:
        #     string += "(Line: {}) ".format(self.line)

        string += "{}".format(self.nemonic)

        if self.arg is not None:
            if self.nemonic == DATA:
                string += " {}".format(self.arg)
            else:
                if type(self.arg) is int:
                    string += " /{:03X}".format(self.arg)
                else:
                    string += " /{}".format(self.arg)

        return string

# ----------- Syntax analyzer


class Parser(object):
    """Sintax analysis"""

    def __init__(self, lexer):
        self.lexer = lexer
        self.prog = Prog_AST()

        # -- The last two token are read in advance
        self.current_token = self.lexer.get_token()
        self.next_token = self.lexer.get_token()

    def error(self, msg=None, line=None):
        raise Exception('Error: {}. Line: {}'.format(msg, line))

    def assert_type(self, type, error_msg="", debug=False):
        """Make sure the current token is of the given type"""

        if self.current_token.type == type:
            if debug:
                print(self.current_token)

            self.current_token = self.next_token
            self.next_token = self.lexer.get_token()

        else:
            self.error(error_msg, line=self.current_token.line)

    def program(self):
        """<program> ::= <lines> "END" EOL"""

        self.lines()
        self.assert_type(END, "END expected")
        self.assert_type(EOL, "No EOL after END")

    def lines(self):
        """<lines> ::= EOL*  (<line> EOL+)* """

        while self.current_token.type not in [EOF, END]:

            self.line()
            self.assert_type(EOL, "Unexpected element")

            # -- Remove the extra EOL (if any)
            while (self.current_token.type == EOL):
                self.assert_type(EOL)

    def line(self):
        """<line> ::= COMMENT | <lineofcode> (COMMENT)"""

        if self.current_token.type == COMMENT:
            self.assert_type(COMMENT)

        else:
            if self.lineofcode():
                if (self.current_token.type == COMMENT):
                    self.assert_type(COMMENT)

    def lineofcode(self):
        """<lineofcode> ::= <directive> | <lineinstruction>"""

        if self.directive():
            return True
        else:
            # -- It is not a directive, should be a instruction
            return self.lineinstruction()

    def directive(self):
        """<directive> ::= <dirORG> | <dirEQU> | <dirRES> | <dirDATA>"""

        if self.dir_org():
            return True
        elif self.dir_equ():
            return True
        elif self.dir_res():
            return True
        elif self.dir_data():
            return True
        else:
            # -- It is not a directive
            return False

    def dir_org(self):
        """<dirORG> ::= ORG NUMBER | ORG LABEL"""

        # -- If it is not an ORG token, return
        if self.current_token.type == ORG:
            self.assert_type(ORG)

            if self.current_token.type == NUMBER:
                addr = self.current_token.value
                self.assert_type(NUMBER)

                # -- Change the current address
                self.prog.addr = addr

            # -- If the address is not a number... it should be a label
            else:
                label = self.current_token.value
                line = self.current_token.line
                self.assert_type(LABEL, "ORG: Label or number expected")

                # -- Get the address asociated to the label
                try:
                    addr = self.prog.symtable[label]
                except KeyError:
                    self.error("Unknow Label: {}".format(label), line=line)

                # -- Change the current address
                self.prog.addr = addr

            return True

        # -- Not an ORG directive
        else:
            return False

    def dir_equ(self):
        """<dirEQU> ::= LABEL EQU NUMBER"""

        if self.current_token.type == LABEL and self.next_token.type == EQU:
            label = self.current_token.value
            line = self.current_token.line
            self.assert_type(LABEL)
            self.assert_type(EQU)
            value = self.current_token.value
            self.assert_type(NUMBER, "EQU: Expected a number")

            # - check if the label is already in the table
            if label in self.prog.symtable:
                self.error(msg="Duplicated label: {}".format(label), line=line)

            # - Insert the label in the symbol table
            self.prog.symtable[label] = value

            return True
        elif self.current_token.type == EQU:
            self.error("EQU without label", line=self.current_token.line)
        else:
            # -- It is not an EQU directive
            return False

    def dir_res(self):
        """<dirRES> ::= (LABEL) RES NUMBER"""

        # -- Case 1:  LABEL RES
        if self.current_token.type == LABEL and self.next_token.type == RES:
            label = self.current_token.value
            line = self.current_token.line
            self.assert_type(LABEL)

            # - check if the label is already in the table
            if label in self.prog.symtable:
                self.error(msg="Duplicated label: {}".format(label), line=line)

            # - Insert the label in the symbol table
            self.prog.symtable[label] = self.prog.addr

        # -- Case 2: RES (without label)
        if self.current_token.type == RES:
            line = self.current_token.line
            self.assert_type(RES)
            value = self.current_token.value
            self.assert_type(NUMBER)

            # -- Reserving 0 words does not make any sense
            if value == 0:
                self.error(msg="Not possible to reserve 0 words", line=line)

            # - Create all the data instructions reserved by the directive res
            for i in range(value):
                instr = Instruction(DATA, line=line, arg=0)
                self.prog.add(instr)

            return True
        else:
            return False

    def dir_data(self):
        """<dirDATA> ::= LABEL DATA <datacollection> |  DATA <datacollection>"""

        # -- Case 1: LABEL DATA
        if self.current_token.type == LABEL and self.next_token.type == DATA:

            # -- Get the label
            label = self.current_token.value
            line = self.current_token.line
            self.assert_type(LABEL)

            # - check if the label is already in the table
            if label in self.prog.symtable:
                self.error(msg="Duplicated label: {}".format(label), line=line)

            # -- Insert the lable in the symbol table
            self.prog.symtable[label] = self.prog.addr

            self.assert_type(DATA)
            self.data_collection()

            return True

        # -- Case 2: DATA (no label)
        if self.current_token.type == DATA:
            self.assert_type(DATA)
            self.data_collection()

            return True

        # -- It is not a DATA directive
        return False

    def data_collection(self):
        """<datacollection> ::= <data> (,<data>)*"""

        self.data()
        while self.current_token.type == COMMA:
            self.assert_type(COMMA)
            self.data()

    def data(self):
        """<data> ::= STRING | NUMBER | LABEL"""

        line = self.current_token.line
        value = self.current_token.value

        if self.current_token.type == NUMBER:
            self.assert_type(NUMBER)
            instr = Instruction(DATA, line=line, arg=value)
            self.prog.add(instr)
        elif self.current_token.type == STRING:
            self.assert_type(STRING)

            # -- Insert one data instruction per character in the string
            for char in value:
                instr = Instruction(DATA, line=line, arg=ord(char))
                self.prog.add(instr)
        elif self.current_token.type == LABEL:
            self.assert_type(LABEL)
            instr = Instruction(DATA, line=line, arg=value)
            self.prog.add(instr)

    def lineinstruction(self):
        """<lineinstruction> ::= (LABEL) <instruction>"""

        if self.current_token.type == LABEL:

            line = self.current_token.line
            label = self.current_token.value

            # - check if the label is already in the table
            if label in self.prog.symtable:
                self.error(msg="Duplicated label: {}".format(label), line=line)

            # - Insert the label in the symbol table
            self.prog.symtable[label] = self.prog.addr

            self.assert_type(LABEL)

            # -- If there is a label, there should be an instrucction
            # -- in the same line
            if self.instruction():
                return True
            else:
                self.error("Invalid instruction", line=line)
                return False

        # -- There should be now an instruction
        line = self.current_token.line
        self.instruction()
        return True

    def instruction(self):
        """<instruction> ::= <instLD>  | <insST>   | <instADD>  | <instBR> |
                             <instBZ>  | <instCLR> | <instDEC> | <instHALT> |
                             <instWAIT>"""

        # -- Case 1: Instructions with no arguments
        for instr in [CLR, DEC, HALT, WAIT]:
            if self.parse_instr0(instr):
                return True

        # -- Case 2: Instructions with 1 argument (an absolute address)
        for instr in [ST, LD, ADD, BR, BZ]:
            if self.parse_instr1(instr):
                return True

        # -- It is not an instruction
        return False

    def parse_instr0(self, inst_type):
        """Parse the instructions with 0 arguments
           HALT, WAIT, DEC, CLR
        """

        if self.current_token.type == inst_type:
            line = self.current_token.line
            self.assert_type(inst_type)
            instr = Instruction(inst_type, line=line)
            self.prog.add(instr)
            return True
        else:
            return False

    def parse_instr1(self, inst_type):
        """Parse the instructions with 1 argument
           ST, LD, ADD, BR, BZ
        """

        if self.current_token.type == inst_type:
            line = self.current_token.line
            self.assert_type(inst_type)
            arg = self.current_token.value
            self.assert_type(ADDR, "Invalid address")
            instr = Instruction(inst_type, arg=arg, line=line)
            self.prog.add(instr)
            return True
        else:
            return False

    def parse(self):
        self.program()
        return self.prog


def parse_arguments():
    """Parse the arguments, open the asm file and return the raw contents"""

    import argparse
    description = """
        Simplez assembler. The prog.list file with the machine code is \
        generated as output
    """
    # -- Add the assembler description
    parser = argparse.ArgumentParser(description=description)

    # -- Add the assembler argument: asmfile
    parser.add_argument("asmfile", help="Simplez asembly file (.asm)")

    # -- Add the assembler argument: verbose
    parser.add_argument("-verbose", help="verbose mode on", action="store_true")

    # -- Output file argument
    parser.add_argument("-o", metavar="output", default=OUTPUT_FILE,
                        help="Specify the output filename")

    # -- Parse the anguments
    args = parser.parse_args()

    # -- File to assembly
    asmfile = args.asmfile

    # -- Output file
    output_file = args.o

    # -- Read the file
    try:
        with open(asmfile, mode='r') as f:
            raw = f.read()
    except:
        print("Error: file not found: {}".format(asmfile))
        sys.exit()

    # -- Return the file and verbose arguments
    return raw, asmfile, output_file, args.verbose


def main():

    # -- Process the arguments. Return the source file and the verbose flags
    asmfile, filename, output_file, verbose = parse_arguments()

    print("Assembler for the SIMPLEZ microprocessor (Version: {})".format(
        VERSION))

    print("Released under the GPL license\n")

    # -- Lexical analysis
    lexer = Lexer(asmfile)

    if verbose:
        print("\n------- Lexical analysis")

        lexer_log = lexer.test()
        print(lexer_log)
        lexer.reset()

        print("\n------- Sintax Analysis ------")

    # -- Syntax analysis
    parser = Parser(lexer)
    try:
        prog = parser.parse()
    except Exception as inst:
        print(inst)
        sys.exit(0)

    if verbose:
        print()
        asmcode1 = prog.assembly()
        print(asmcode1)
        print("Symbols:")
        prog.show_symbols()

        print()
        print("-------- Semantics analysis:")

    try:
        prog.solve_labels()
    except Exception as inst:
        print(inst)
        sys.exit(0)

    if verbose:
        asmcode2 = prog.assembly()
        print(asmcode2)

        print("-------- Generated machine code")

    mcode = ""
    mcode += "//-- Source file: {}\n".format(filename)
    mcode += "//-- Output file format: verilog\n\n"
    mcode += prog.machine_code(asm=True)

    if verbose:
        print(mcode)

    # -- Write the machine code in the output file file
    with open(output_file, mode='w') as f:
        f.write(mcode)

    print("OK! Machine code for SIMPLEZ generated\n")
    print("File: {}".format(output_file))
    scode, sdata = prog.size()
    print("Size:   {} words".format(scode + sdata))
    print("  Code: {} words".format(scode))
    print("  data: {} words".format(sdata))

# -- Main program
if __name__ == '__main__':
    main()
