# - Simplez assembler
# - Grammar definition
# -
# --- A program is a list of lines with the END keyword in the end (finished by EOL)
# --- Notice that after the END there could be more instructions, but they will be ignored
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
# -- All the instruction can have a label in the beginning of the line (optionally)
# <lineinstruction> ::= <instruction> | LABEL <instruction>
#
# -- There are 9 different simplez-F instructions
# <instruction> ::= <instLD>  | <insST>   | <instADD>  | <instBR> | <instBZ> |
# ----------------- <instCLR> | <instDEC> | <instHALT> | <instWAIT>
#

# - There are 4 different directives
# <directive> ::= <dirORG> | <dirEQU> | <dirRES> | <dirDATA>
#
# - ORG directive do not have any label in the left. The argument can be a number or a label
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
(EOL, EOF, COMMENT, LABEL, ORG, NUMBER, STRING, ADDRNUM, ADDRLABLE,
 LD, ST, ADD, BR, BZ, CLR, DEC, HALT, WAIT, UNKNOWN, END) = (
 'EOL', 'EOF', 'COMMENT', 'LABEL', 'ORG', 'NUMBER', 'STRING', 'ADDRNUM', 'ADDRLABLE',
 'LD', 'ST', 'ADD', 'BR', 'BZ', 'CLR', 'DEC', 'HALT', 'WAIT', 'UNKNOWN', 'END'
)

DEBUG_PARSER = True


class Token(object):
    """Token generator"""

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        if self.type == COMMENT:
            return "Token: COMMENT: \"{}\" ".format(self.value)
        elif self.type in [EOL, EOF, END, ORG]:
            return "Token: {}".format(self.type)
        elif self.type in [NUMBER, LABEL]:
            return "Token: {} ({})".format(self.type, self.value)
        else:
            return "Token: Unknown ({})".format(self.value)


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


class Lexer(object):
    """Lexical analyzer"""

    def __init__(self, text):
        self.text = text.upper()
        self.pos = 0
        self.line = 1

    def reset(self):
        self.pos = 0
        self.line = 1

    def check_hexnumber(self):
        """Check if it is an hexadecimal number. If so, return its value, else None"""
        scan = re.match(REGEX_HEX, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())

            # -- Return the number
            return int(scan.group()[2:], 16)
        else:
            return None

    def check_decimal(self):
        """Check if it is a decimal number. If so, return it svalue, else None"""

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

    def check_directive(self):
        """Check if it is a directive"""

        for direct in [END, ORG]:
            scan = re.match(direct, self.text[self.pos:])
            if scan:
                self.pos += len(scan.group())
                return direct

    def check_label(self):
        """Check if it is a label"""

        scan = re.match(REGEX_LABEL, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())
            return scan.group()

    def get_token(self):
        """Get the next token from tex"""

        # -- Remove the white spaces (except \n)
        scan = re.match(REGEX_WSPACE, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())

        # -- Is it a commnet?
        comment = self.check_comment()
        if comment:
            return Token(COMMENT, comment)

        # -- Is it a hexadecimal number?
        hexnumber = self.check_hexnumber()
        if hexnumber is not None:
            return Token(NUMBER, hexnumber)

        # -- Is it a decimal number?
        number = self.check_decimal()
        if number is not None:
            return Token(NUMBER, number)

        # -- Check if it is a directive
        direct = self.check_directive()
        if direct:
            return Token(direct, None)

        # -- Check if it is a label
        label = self.check_label()
        if label:
            return Token(LABEL, label)

        # --Get the current char
        try:
            current_char = self.text[self.pos]
        except IndexError:
            return Token(EOF, None)

        # -- Is it a EOL?
        if current_char == '\n':
            self.pos += 1
            self.line += 1
            return Token(EOL, None)

        self.pos += 1
        return Token(UNKNOWN, current_char)

    def test(self):
        """Test the lexer"""
        while True:
            line = self.line
            token = self.get_token()
            print("Line: {}  {}".format(line, token))
            if token.type == EOF:
                return


class Parser(object):
    """Sintax analysis"""

    def __init__(self, lexer):
        self.lexer = lexer

        # -- The last two token are read in advance
        self.current_token = self.lexer.get_token()
        self.next_token = self.lexer.get_token()

    def error(self, msg=""):
        raise Exception('Error parsing input: {}. Line: {}'.format(msg, self.lexer.line))

    def assert_type(self, type, error_msg="", debug=False):
        """Make sure the current token is of the given type"""

        if self.current_token.type == type:
            if debug:
                print(self.current_token)

            self.current_token = self.next_token
            self.next_token = self.lexer.get_token()

        else:
            self.error(error_msg)

    def program(self):
        """<program> ::= <lines> "END" EOL"""

        self.lines()
        self.assert_type(END, "END expected")
        self.assert_type(EOL, "No EOL after END")

    def lines(self):
        """<lines> ::=  (<line> EOL+)* """

        while self.current_token.type not in [EOF, END]:
            self.line()
            self.assert_type(EOL, "No EOL after line")

            # -- Remove the extra EOL (if any)
            while (self.current_token.type == EOL):
                self.assert_type(EOL)

    def line(self):
        """<line> ::= COMMENT | <lineofcode> (COMMENT)"""

        if self.current_token.type == COMMENT:

            if DEBUG_PARSER:
                print("Comment line: {}".format(self.current_token.value))

            self.assert_type(COMMENT)

        else:
            self.lineofcode()
            if (self.current_token.type == COMMENT):
                self.assert_type(COMMENT)

    def lineofcode(self):
        """<lineofcode> ::= <directive> | <lineinstruction>"""

        self.directive()

    def directive(self):
        """<directive> ::= <dirORG> | <dirEQU> | <dirRES> | <dirDATA>"""

        if self.dir_org():
            return True
        elif self.dir_equ():
            return True
        else:
            return False

    def dir_org(self):
        """<dirORG> ::= ORG NUMBER | ORG LABEL"""

        # -- If it is not an ORG token, return
        if self.current_token.type == ORG:
            self.assert_type(ORG)

            if self.current_token.type == NUMBER:
                addr = self.current_token.value
                self.assert_type(NUMBER)

                if DEBUG_PARSER:
                    print("ORG {}".format(addr))

            # -- If the address is not a number... it should be a label
            else:
                label = self.current_token.value
                self.assert_type(LABEL)

                if DEBUG_PARSER:
                    print("ORG {}".format(label))

            return True

        # -- Not an ORG directive
        else:
            return False

    def dir_equ(self):
        """<dirEQU> ::= LABEL EQU NUMBER"""

        print(self.current_token)
        print(self.next_token)

    def parse(self):
        self.program()
        print("PARSING OK!")
        return


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

    # -- Parse the anguments
    args = parser.parse_args()

    # -- File to assembly
    asmfile = args.asmfile

    # -- Read the file
    try:
        with open(asmfile, mode='r') as f:
            raw = f.read()
    except:
        print("Error: file not found: {}".format(asmfile))
        sys.exit()

    # -- Return the file and verbose arguments
    return raw.upper(), args.verbose


# -- Main program
if __name__ == '__main__':

    # -- Process the arguments. Return the source file and the verbose flags
    asmfile, verbose = parse_arguments()

    lexer = Lexer(asmfile)
    lexer.test()
    lexer.reset()

    # - Parser
    print("\n------- Sintax Analysis ------")
    parser = Parser(lexer)
    parser.parse()
