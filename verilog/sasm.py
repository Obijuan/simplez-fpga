# ---------------------------------------------------------------------------------
# --  Asembler for the Simplez microprocessor
# --  (C) BQ November 2015. Written by Juan Gonzalez (obijuan)
# --  Python 3
# ----------------------------------------------------------------------------------
# -- Released under the GPL v3 License
# ----------------------------------------------------------------------------------
import sys


class Prog(object):
    """Abstract syntax Tree for the assembled program"""

    def __init__(self):
        self._addr = 0   # -- Current address
        self.linst = []  # -- List of instructions

        # -- Symbol table. It is used for storing the pairs label - address
        self.symtable = {}


class Instruction(object):
    """Microbio instruction class"""

    # -- Instruction opcodes
    opcodes = {"WAIT": 0, "HALT": 1, "LEDS": 2, "JP": 3}

    def __init__(self, nemonic, dat=0, addr=0, label="", nline=0):
        """Create the instruction from the co and dat fields"""
        self.nemonic = nemonic  # -- Instruction name
        self._dat = dat     # -- Instruction argument
        self.addr = addr    # -- Address where the instruction is stored in memory
        self.label = label  # -- Label (if any)
        self.nline = nline  # -- Line number


class SyntaxError(Exception):
    """Syntax error exceptions"""
    def __init__(self, msg, nline):
        self.msg = msg        # - Sintax error message
        self.nline = nline    # - Number of line were the sintax error is located


def is_comment(word):
    """Return True if the word is a commnet"""

    # -- At least the string len should be 2 for being a comment
    if len(word) < 2:
        return False

    comment = word[0:2]
    if (comment == "//"):
        return True
    else:
        return False


def is_blank_line(line):
    """Returns true if the line is blank"""

    # -- Divide the line into a list of words
    words = line.split()

    # -- If it is a blank line, ignore it
    if len(words) == 0:
        return True
    else:
        return False


def is_comment_line(line):
    """Returns true if the line is a commnet"""
    # -- Divide the line into a list of words

    words = line.split()

    # - It is a commnet line if the first words is a comment
    return is_comment(words[0])


def syntax_analisis(prog, asmfile):
    """Perform the syntax analisis
        prog: AST with the processed program (outuput)
        asmfile: ASCII raw file (input)
    """

    # -- Split the ASCII file into isolates lines
    asmfile = asmfile.splitlines()

    # -- DEBUG: show all the program lines
    print("Complete program:")
    for nline, line in enumerate(asmfile):
        print("[{}] {}".format(nline+1, line))

    # -- Syntax analisis: line by line
    print("\nPass 1:")
    for nline, line in enumerate(asmfile):

        # - Remove blank lines
        if is_blank_line(line):
            continue

        # - Remove lines that only have comments
        if is_comment_line(line):
            continue

        print("[{}] {}".format(nline+1, line))


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


if __name__ == "__main__":
    """Main program"""

    # -- default output file with the machine code for MICROBIO
    OUTPUT_FILE = "prog.list"

# -- Process the arguments. Return the source file and the verbose flags
    asmfile, verbose = parse_arguments()

    # -- Create a blank AST for storing the processed program
    prog = Prog()

    print("Assembler for the SIMPLEZ microprocessor")
    print("Released under the GPL license\n")

    # -- Perform the sintax analisis. The sintax errors are reported
    # -- In case of errors, it exits
    # -- If sucess, the program is stored in the prog object
    syntax_analisis(prog, asmfile)
