#!/usr/bin/python3
import sys
import re


# -- It was part of the v1.0 sasm.py
class Lexer(object):
    """General functions for parsing"""

    # - Symbol used for defining comments in the assembler
    # - It is a parameter. It can be changed
    # COMMENT_SYMBOL = "//"  # - C / Verilog style
    # COMMENT_SYMBOL = "#"  # - Python style
    COMMENT_SYMBOL = ";"

    # Symbols for representing hexadecimal numbers
    # SYM_HEX = "0x"  # - Notation in C / python style
    SYM_HEX = "H'"  # - Notation in Simlez

    # Regular expresions for Parsing Hexadecimal numbers
    # - In Simplez, hexadecimal numbers are written as: H'8A, H'960A, etc
    REGEX_HEX = r"^{}[0-9a-fA-F]+$".format(SYM_HEX.upper())

    @staticmethod
    def is_comment(word):
        """Return True if the word is a comment"""

        # - Split the word usign the COMMENT_SYMBOL
        words = word.split(Lexer.COMMENT_SYMBOL)

        # - It does not contains the comment symbol
        if (len(words) == 1):
            return False

        # - The first word should be null (no charcters before the
        # - comment symbol)
        if (len(words[0]) == 0):
            return True
        else:
            return False

    @staticmethod
    def is_comment_line(line):
        """Returns true if the whole line is a comment"""

        # -- Divide the line into a list of words
        words = line.split()

        # - It is a commnet line if the first words is a comment
        return Lexer.is_comment(words[0])

    @staticmethod
    def is_blank_line(line):
        """Returns true if the line is blank"""

        # -- Divide the line into a list of words
        words = line.split()

        # -- If it is a blank line, ignore it
        if len(words) == 0:
            return True
        else:
            return False

    @staticmethod
    def is_hexdigit(word):
        """Returns True if words is an ASCII hexadecimal number"""

        if re.search(Lexer.REGEX_HEX, word):
            return True
        else:
            return False

    @staticmethod
    def is_number(word):
        """Determine if the word is a number (in decimal) or in hexadecimal
           It returns:
           -True: is a number
           -False: is not a number"""
        return word.isdigit() or Lexer.is_hexdigit(word)


class SyntaxError(Exception):
    """Syntax error exceptions"""
    def __init__(self, msg, nline):
        self.msg = msg       # - Sintax error message
        self.nline = nline   # - Number of line were the sintax error is located


class Test_progs(object):
    """Program example 1: adding two numbes"""
    SIMPLEZ1 = [0x0, 0x205, 0x406, 0x007, 0xE00, 0x007, 0x008, 0x00]

    """Program example 2: Sum of the 10 term of the fibonacci serie"""
    SIMPLEZ2 = [0xA00, 0x02F, 0x233, 0x030, 0x032, 0x234, 0x02E, 0x22F, 0x430,
                0x031, 0x432, 0x032, 0x230, 0x02F, 0x231, 0x030, 0x22E, 0xC00,
                0x815, 0x02E, 0x607, 0x232, 0xE00,     0,     0,     0,     0,
                0,         0,     0,     0,     0,     0,     0,     0,     0,
                0,         0,     0,     0,     0,     0,     0,     0,     0,
                0,         0,     0,     0,     0,     0,     1,     8,     0,
                0,         0,     0,     0,     0,     0,
                ]


class simplez(object):
    """Simplez simulator"""

    NEMONIC = ["ST", "LD", "ADD", "BR", "BZ", "CLR", "DEC", "HALT"]
    OP_ST = 0
    OP_LD = 1
    OP_ADD = 2
    OP_BR = 3
    OP_BZ = 4
    OP_CLR = 5
    OP_DEC = 6
    OP_HALT = 7

    # -- Extended opcodes
    XOP_HALT = 0xE
    XOP_WAIT = 0xF

    # -- States for the processor
    INIT = 0  # - Initial state (no instruction executed yet)
    RUNNING = 1  # - Simulating
    STOPED = 2  # - Micro stopped. Halt instruction executed

    def __init__(self):
        self._A = 0   # - A register
        self._PC = 0  # - Program counter
        self._Z = 0   # - Z flag
        self._mem = [0 for i in range(512)]  # - Simplez memory
        self.state = self.INIT  # - Processor state
        self._vars = {}  # - Dictionary of selected variables to show
        self._load_addr = 0  # - Address for loading the machine code

    def _decode(self, inst):
        """Return the opcode and argument of a given instruction
           in machine code"""
        return (inst >> 9, inst & 0x1FF)

    def show(self):
        print("PC = H'{:03X}".format(self._PC))
        print("A = H'{:03X}".format(self._A))
        print("Z = {}".format(self._Z))
        self.vars()
        if self.state == self.STOPED:
            print("Micro stopped! Halt executed")
        else:
            # - Fetch the current instruction
            ir = self._mem[self._PC]

            # - Print the current instruction
            print("Next: [{:03X}] {}".format(self._PC, self._code2asm(ir)))

    def load(self, prog):
        """Load a program into the memory. The program consist of a
           list of consecutive instructions"""

        l = len(prog)
        self._mem[0:l] = prog

    def mem(self, nblocks=32):
        """Print the memory
           nblocks = number of blocks (of 16 words) to print"""
        print("       0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F")
        for block in range(nblocks):
            linecode = ""
            for pos in self._mem[(block * 16):(block*16 + 16)]:
                linecode += "{:03X} ".format(pos)

            print("[{:03X}] {}".format(block*16, linecode))

    def vars(self):
        """Show the current vars"""
        for addr, label in self._vars.items():
            # - Read the variable value from memory
            value = self._mem[addr]

            # - Show the variable
            print("[{0:03X}] {1} = H'{2:03X} ({2})".format(addr, label, value))

    def add_var(self, varname, varaddr):
        """Add the pair varname (string) and address
           varname: String with the given name to the variable
           varaddr: The address were the variable is stored
        """
        # -- Add the var to the dictionary
        # -- TODO: check for duplicates!
        self._vars[varaddr] = varname.upper()

    def list(self, ninst=10, addr_ini=0):
        """List the memory as assembly code
           ninst: Number of instructions to show
           addr_ini: Initial address
        """
        for addr in range(addr_ini, addr_ini + ninst):
            # - Fetch the instruction from memory
            inst = self._mem[addr]
            print("[{:03X}] {}".format(addr, self._code2asm(inst)))

    def _execute(self, opcode, addr, xopcode):
        """Execute the give instruction"""

        if opcode == self.OP_ST:
            self._mem[addr] = self._A

        elif opcode == self.OP_LD:
            self._A = self._mem[addr]

        elif opcode == self.OP_ADD:
            self._A += self._mem[addr]

        elif opcode == self.OP_CLR:
            self._A = 0

        elif opcode == self.OP_DEC:
            self._A -= 1

        elif opcode == self.OP_BR:
            self._PC = addr

        elif opcode == self.OP_BZ:
            if self._Z == 1:
                self._PC = addr

        elif opcode == self.OP_HALT:
            """Check the extended instructions"""
            print("HALT. xopcode: {}".format(xopcode))
            if xopcode == self.XOP_HALT:
                self.state = self.STOPED

    def _single_step(self):
        """Simulate only the next instruction"""
        # - Fetch the current instruction
        ir = self._mem[self._PC]

        # - Print the current instruction
        print("Executing: [{:03X}] {}".format(self._PC, self._code2asm(ir)))

        # - Point to the next instruction
        self._PC += 1

        # - Decode the instruction
        opcode, addr = self._decode(ir)

        # - Decode de extended instructions
        xopcode = ir >> 8

        # - Execute
        self._execute(opcode, addr, xopcode)

        # - Update the Z flag
        if self._A == 0:
            self._Z = 1
        else:
            self._Z = 0

    def run(self):
        """Simulate the program until the end """

        # -- Show info of the initial state
        if self.state == self.INIT:
            print("Initial state:")
            self.show()
            print()
            self.state = self.RUNNING

        # - Simulate the whole program
        while self.state != self.STOPED:
            self._single_step()

        # - Show the final resultas
        self.show()

    def step(self, nsteps=1):
        """Simulate the given steps"""

        if self.state == self.INIT:
            print("Initial state:")
            self.show()
            print()
            self.state = self.RUNNING

        # -- Simulate nsteps
        for i in range(nsteps):
            if self.state == self.STOPED:
                print("Micro stopped! Halt executed")
                return
            self._single_step()
            self.show()

    def _is_mcode_line(self, line):
        """Return true if it is sintactically correct machine code line"""

        words = line.split()

        # -- First word should be a hexadecimal digit
        if re.search("^[0-9a-fA-F]+", words[0]):

            # - The next word (if any) should be a comment
            if (len(words) > 1):
                if Lexer.is_comment(words[1]):
                    return True
                else:
                    # -- Not a comment. Is not a correct mcode line
                    return False

            return True
        else:
            return False

    def _is_addr_line(self, line):
        words = line.split()

        # -- First word should be a @ + hexadecimal digit
        if re.search("^@[0-9a-fA-F]+", words[0]):

            # - The next word (if any) should be a comment
            if (len(words) > 1):
                if Lexer.is_comment(words[1]):
                    return True
                else:
                    # -- Not a comment. Is not a correct mcode line
                    return False

            return True
        else:
            return False

    def _parse_mcode(self, line):
        words = line.split()

        # - If is a correct machine code (only sintax)
        if self._is_mcode_line(line):

            # - Get the machine code word
            mcode = int(words[0], 16)

            # - Write the machine code in the memory, in the current addr
            self._mem[self._load_addr] = mcode
            self._load_addr += 1

            # print("{:03X}".format(mcode))

        # - Check if is an address code (@xxx)
        elif self._is_addr_line(line):
            addr = int(words[0][1:], 16)
            self._load_addr = addr
            # print("@{:03X}".format(addr))

        else:
            msg = "\nSINTAX ERROR. Unkwown line:\n{}".format(line)
            raise SyntaxError(msg, 0)

    def load_mcode_file(self, filename):
        """Open a file with the machine code. Parse it. Returns the a list with
           all the machine codes"""

        Lexer.COMMENT_SYMBOL = "//"

        # - Start loading from the addr 0
        self._load_addr = 0

        # -- Read the file
        try:
            with open(filename, mode='r') as f:
                raw = f.read()
        except:
            print("Error: file not found: {}".format(filename))
            sys.exit()

        # REGEX_MCODE = r"[0-9a-fA-F]+"

        # -- Split the ASCII file into isolates lines
        raw = raw.splitlines()
        for line in raw:
            # - Remove blank lines
            if Lexer.is_blank_line(line) or Lexer.is_comment_line(line):
                continue

            try:
                self._parse_mcode(line)
            except SyntaxError as e:
                print(e.msg)
                sys.exit()

        print("\nprog.list loaded into memory!")

    def _code2asm(self, inst):
        """Return a string with the given machine code instruction
           in assembly language"""

        opcode, addr = self._decode(inst)
        nemonic = self.NEMONIC[opcode]
        asm = "{}".format(nemonic)

        # - Add the argument
        if nemonic in ["ST", "LD", "ADD", "BR", "BZ"]:
            asm += " /H'{:03X}".format(addr)

        # - Add the content of the memory (as a comment)
        if nemonic in ["ST", "LD", "ADD"]:
            asm += ";  [{:03X}]={:03X}".format(addr, self._mem[addr])

        return asm


def example_simplez2(s):
    """Example of simulation of the program SIMPLEZ2"""

    # - Load the machine code
    # s.load(Test_progs.SIMPLEZ2)

    # - Add the variables to watch (label - address)
    s.add_var("cont", 46)
    s.add_var("pen", 47)
    s.add_var("ult", 48)
    s.add_var("sig", 49)
    s.add_var("SUM", 50)


def example_simplez3(s):
    s.add_var("SUM", 150)


def example_simplez4(s):
    s.add_var("cien", 100)
    s.add_var("doscientas", 200)
    s.add_var("cont", 3)
    s.add_var("temp", 4)


def example_simplez5(s):
    s.add_var("res1", 52)
    s.add_var("res2", 102)
    s.add_var("resta", 201)
    s.add_var("arg", 202)


def main():

    # - Create the virtual simplez processor
    s = simplez()

    # -- Load the machine code to simulate
    s.load_mcode_file("prog.list")

    # -- Simulate the SIMPLEZ2 example
    # example_simplez5(s)

if __name__ == "__main__":
    """Main program"""

    main()
