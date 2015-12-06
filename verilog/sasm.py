# ---------------------------------------------------------------------------------
# --  Asembler for the Simplez microprocessor
# --  (C) BQ November 2015. Written by Juan Gonzalez (obijuan)
# --  Python 3
# ----------------------------------------------------------------------------------
# -- Released under the GPL v3 License
# ----------------------------------------------------------------------------------
import sys
import re


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

    def is_comment(word):
        """Return True if the word is a comment"""

        # - Split the word usign the COMMENT_SYMBOL
        words = word.split(Lexer.COMMENT_SYMBOL)

        # - It does not contains the comment symbol
        if (len(words) == 1):
            return False

        # - The first word should be null (no charcters before the comment symbol)
        if (len(words[0]) == 0):
            return True
        else:
            return False

    def is_comment_line(line):
        """Returns true if the whole line is a comment"""

        # -- Divide the line into a list of words
        words = line.split()

        # - It is a commnet line if the first words is a comment
        return Lexer.is_comment(words[0])

    def is_blank_line(line):
        """Returns true if the line is blank"""

        # -- Divide the line into a list of words
        words = line.split()

        # -- If it is a blank line, ignore it
        if len(words) == 0:
            return True
        else:
            return False

    def is_hexdigit(word):
        """Returns True if words is an ASCII hexadecimal number"""

        if re.search(Lexer.REGEX_HEX, word):
            return True
        else:
            return False


class Prog(object):
    """Abstract syntax Tree (AST) for the assembled program"""

    RESERVED_WORDS = ["ST", "LD", "ADD", "BR", "BZ", "CLR", "DEC", "HALT",  "WAIT",
                      "ORG", "DATA"]

    def __init__(self):
        self._addr = 0   # -- Current address
        self.linst = []  # -- List of instructions

        # -- Symbol table. It is used for storing the pairs label - address
        self.symtable = {}

    def add_instruction(self, inst):
        """Add the instruction in the current address. The current dir is incremented
        """

        # -- Assign the current address
        inst.addr = self._addr

        # -- Insert the instruction
        self.linst.append(inst)

        # -- Increment the current address
        self._addr += 1

    def is_label(self, word):
        """Return True if the word is a label"""

        # - it is a label if it is NOT a reserved word or
        # - a number

        # - It is a number (decirmal or hexadecila. It is NOT a label)
        if word.isdigit() or Lexer.is_hexdigit(word):
            return False

        # - It is a reserved word: not a label!
        if word in self.RESERVED_WORDS:
            return False

        # - It should be a label
        return True

    def set_label(self, label, nline):
        """Assign the label to the current address"""

        if label in self.symtable:
            msg = "ERROR. Label {} is duplicated in line {}".format(label, nline)
            raise SyntaxError(msg, 0)
        else:
            self.symtable[label] = self._addr

    def assign_labels(self):
        """Check all the labels of the JP instructions of the program
           to make sure they all have an address asigned. If not, the attribute addr
           is updated with the right value
           If there are unknown labels an exception is raised
        """
        for inst in self.linst:
            if inst.nemonic in ["LD", "BR", "BZ", "ST", "ADD"]:
                try:
                    if len(inst.label) != 0:
                        inst._dat = prog.symtable[inst.label]
                except KeyError:
                    msg = "ERROR: Label {} unknow in line {}".format(inst.label, inst.nline)
                    raise SyntaxError(msg, inst.nline)

    def set_addr(self, addr):
        """Set the current address"""
        self._addr = addr

    def get_addr(self):
        """Return the current address"""
        return self._addr

    def __str__(self):
        """Print the current program (in assembly language)"""

        # -- Calculate the length of the longest label
        labels = list(self.symtable.keys())
        lenlabels = list(map(len, labels))
        maxlen = max(lenlabels)

        str = ""
        addr = 0

        for inst in self.linst:
            if addr != inst.addr:
                # -- there is a gap in the addresses
                str += "\n"
                str += " " * (maxlen + 8)
                str += "ORG {0}{1:03X}\n".format(Lexer.SYM_HEX, inst.addr)
                addr = inst.addr

            str += "{}\n".format(inst.get_asmstr(symtable=self.symtable))
            addr += 1

        return str

    def machine_code(self):
        """Generate the program in simplez machine code"""

        # -- Calculate the length of the longest label
        labels = list(self.symtable.keys())
        if len(labels) == 0:
            maxlen = 0
        else:
            lenlabels = list(map(len, labels))
            maxlen = max(lenlabels)

        addr = 0
        code = ""
        for inst in self.linst:
            inst_ascii = ""
            if addr != inst.addr:
                # -- There is a gap in the addresses
                inst_ascii = "\n@{0:03X}  //-- ".format(inst.addr)
                inst_ascii += " " * (8 + maxlen)
                inst_ascii += "ORG 0x{0:03X}\n".format(inst.addr)
                addr = inst.addr

            inst_ascii += "{:03X}   //-- {}".format(inst.mcode(), inst.get_asmstr(self.symtable))
            code += inst_ascii + "\n"
            addr += 1

        return code


class Instruction(object):
    """Microbio instruction class"""

    # -- Instruction opcodes
    opcodes = {"ST": 0, "LD": 1, "ADD": 2, "BR": 3, "BZ": 4,
               "CLR": 5, "DEC": 6, "HALT": 7, "WAIT": 0xF,
               "DATA": 0xFF, }

    def __init__(self, nemonic, dat=0, addr=0, label="", nline=0):
        """Create the instruction from the co and dat fields"""
        self.nemonic = nemonic  # -- Instruction name
        self._dat = dat     # -- Instruction argument
        self.addr = addr    # -- Address where the instruction is stored in memory
        self.label = label  # -- Label (if any)
        self.nline = nline  # -- Line number

    def opcode(self):
        """Return the instruction opcode"""
        return self.opcodes[self.nemonic]

    def mcode(self):
        """Return the machine code"""
        if self.nemonic == "DATA":
            return self._dat
        elif self.nemonic == "WAIT":
            return 0xF00
        else:
            return (self.opcode() << 9) + self._dat

    def get_asmstr(self, symtable):
        """Print the instruction in assembly"""

        # -- Calculate the length of the longest label
        labels = list(symtable.keys())
        if len(labels) == 0:
            maxlen = 0
        else:
            lenlabels = list(map(len, labels))
            maxlen = max(lenlabels)

        # -- String for the address
        saddr = "[{:03X}]".format(self.addr)

        # -- Check if the argument has a label associated
        if self._dat in symtable.values():
            index = list(symtable.values()).index(self._dat)
            sarg = "/{0} {1}-- {0} = {2}{3:03X} ".format(list(symtable.keys())[index],
                                                         Lexer.COMMENT_SYMBOL,
                                                         Lexer.SYM_HEX,
                                                         self._dat)
        else:
            sarg = "/{0}{1:03X}".format(Lexer.SYM_HEX, self._dat)

        # - Check if the current address has a label associated to it
        if self.addr in symtable.values():
            index = list(symtable.values()).index(self.addr)
            label = list(symtable.keys())[index]
            saddr += "[{}]".format(label)
            saddr += " " * (maxlen - len(label))
        else:
            # - Calculate the length of the longest label
            saddr += " " * (maxlen + 2)

        if self.nemonic in ["LD", "BR", "BZ", "ST", "ADD"]:
            return "{} {} {}".format(saddr, self.nemonic, sarg)
        elif self.nemonic == "DATA":
            return "{0} DATA {1}{2:03X}".format(saddr, Lexer.SYM_HEX, self._dat)
        else:
            return "{} {}".format(saddr, self.nemonic)


class SyntaxError(Exception):
    """Syntax error exceptions"""
    def __init__(self, msg, nline):
        self.msg = msg        # - Sintax error message
        self.nline = nline    # - Number of line were the sintax error is located


def is_number(word):
    """Determine if the word is a number (in decimal) or in hexadecimal
       It returns:
       -True: is a number
       -False: is not a number"""
    return word.isdigit() or Lexer.is_hexdigit(word)


def parse_dat(dat, nline):
    """Parse a numerical data
       * Returns (ok, dat)
          -ok: True: Successfully parsed
          -dat: Numerical data
    """

    if dat.isdigit():
        return True, int(dat)

    if Lexer.is_hexdigit(dat):

        # -- Convert the string into number
        try:
            hex = int(dat[2:], 16)
        except ValueError:
            msg = "ERROR: Invalid hexadecimal number in line {}".format(nline)
            raise SyntaxError(msg, nline)

        return True, hex

    # -- Not a number
    return False, 0


def parse_label(prog, label, nline):
    """Parse the label and added it to the symbol table
        INPUTS:
        - prog: AST tree where the current program is being processed
        - label: A string to parse

        Returns:
        -TRUE: If it is a label
        -False: Not a label
    """
    if prog.is_label(label):
        # -- Inset the label in the symbol table
        prog.set_label(label, nline)
        return True
    else:
        return False


def parse_org(prog, words, nline):
    """Parse the org directive
        Inputs:
          * prog: AST tree were to store the information obtained from parsing the line
          * words: List of words to parse
          * nline: number of the line that is being parsed

        Returns:
          * False, If it is not an org directive
          * True. Success
          * An exception is raised in case of a sintax error
    """

    # -- The first word is not ORG. It is not an org directive
    if not words[0] == "ORG":
        return False

    # -- Sintax error: The org directive should have one argument with the address
    if len(words) == 1:
        msg = "ERROR: No address is given after ORG in line {}".format(nline)
        raise SyntaxError(msg, nline)

    # -- Read the argument. It should be a number
    okdat, dat = parse_dat(words[1], nline)

    # -- Invalid data
    if not okdat:
        msg = "ERROR: ORG {}: Invalid address in line {}".format(words[1], nline)
        raise SyntaxError(msg, nline)

    # -- Update the current address. The next instruction will be stored in this
    # -- address
    prog.set_addr(dat)

    # -- Get the following words if any. They should only be comments
    words = words[2:]

    # -- If no more words to parse, return
    if len(words) == 0:
        return True

    # -- If there are comments, return true. If they are not comments, there
    # -- is a sintax error
    if Lexer.is_comment(words[0]):
        return True
    else:
        msg = "Syntax error in line {}: Unknow command {}".format(nline, words[0])
        raise SyntaxError(msg, nline)


def parse_dir(prog, word, nline):
    """Parse the address argument"""

    # -- Check the address mode. For simplez is always absolute
    if word[0] != "/":
        msg = "ERROR: Invalid argument {} for instruction in line {}".format(word, nline)
        msg += "\nIt should be an absolute direction (/)"

        raise SyntaxError(msg, nline)

    # -- Remove the / symbol
    word = word[1:]

    # -- The next string could be a number ...
    if is_number(word):
        # -- Read the data
        okdat, dat = parse_dat(word, nline)

        # -- It returns the address and blank label
        return dat, ""

    # -- Or a label
    if prog.is_label(word):

        # -- It returns the address 0 and the label
        return 0, word


def parse_instruction_data(prog, words, nline):
        """Parse the DATA assembler directive
            INPUTS:
              -prog: AST tree where to insert the parsed instruction
              -words: List of words to parse
              -nline: Number of the line that is beign parsed

            RETURNS:
              -True: Success. Instruction parsed and added into the AST
              -False: Not data directive
              -An exception is raised in case of a syntax error
        """
        # -- Parse the LEDS instruction
        if words[0] == "DATA":

            # -- Read the data
            okdat, dat = parse_dat(words[1], nline)

            # -- Invalid data
            if not okdat:
                msg = "ERROR: Invalid data for the instruction {} in line {}".format(
                       words[0], nline)
                raise SyntaxError(msg, nline)

            # -- Create the instruction
            inst = Instruction(words[0], dat)

            # -- Insert in the AST tree
            prog.add_instruction(inst)

            return True

        else:
            return False


def parse_instruction_arg1(prog, words, nline):
    """Parse the instruction with 1 argument: LD, ST ...and insert into the prog AST tree
        INPUTS:
          -prog: AST tree where to insert the parsed instruction
          -words: List of words to parse
          -nline: Number of the line that is beign parsed

        RETURNS:
          -True: Success. Instruction parsed and added into the AST
          -False: Not an instruction
          -An exception is raised in case of a sintax error
    """
    # -- Check that there are at least 2 words in the line (1 for the nemonic and
    # -- one for the argument. If not, raise an exception)
    if len(words) == 1:
        msg = "ERROR: No data for the instruction {} in line {}".format(words[0], nline)
        raise SyntaxError(msg, nline)

    # -- Check if there is a data assembler directive
    parse_instruction_data(prog, words, nline)

    # -- Check if it is a instruction with 1 argument
    if words[0] in ["ST", "LD", "ADD", "BR", "BZ"]:

        # -- Read the address argument
        dat, label = parse_dir(prog, words[1], nline)

        # -- Create the instruction
        inst = Instruction(words[0], dat=dat, label=label, nline=nline)

        # -- Insert in the AST tree
        prog.add_instruction(inst)

    # -- Parse the comments, if any
    words = words[2:]

    # -- If no more words to parse, return
    if len(words) == 0:
        return True

    # -- There can only be comments. If not, it is a syntax error
    if Lexer.is_comment(words[0]):
        return True
    else:
        msg = "Syntax error in line {}: Unknow command".format(nline)
        raise SyntaxError(msg, nline)

    return False


def parse_instruction_arg0(prog, words, nline):
    """Parse the instructions with no arguments: HALT and WAIT
        INPUTS:
          -prog: AST tree where to insert the parsed instruction
          -words: List of words to parse
          -nline: Number of the line that is beign parsed

        RETURNS:
          -True: Success. Instruction parsed and added into the AST
          -False: Not the LEDS instruction
          -An exception is raised in case of a syntax error
    """
    if words[0] in ["HALT", "WAIT", "CLR", "DEC"]:

        # -- Create the instruction from the nemonic
        inst = Instruction(words[0])

        # -- Insert it in the AST tree
        prog.add_instruction(inst)

        # -- Check that there are only comments or nothing after these nemonics
        words = words[1:]

        # -- If no more words to parse, return
        if len(words) == 0:
            return True

        if Lexer.is_comment(words[0]):
            return True
        else:
            msg = "Syntax error in line {}: Unknow command".format(nline)
            raise SyntaxError(msg, nline)
            return False
    else:
        # -- The instructions are not HALT or WAIT
        return False


def parse_instruction(prog, words, nline):
    """Parse the instruction and insert into the prog AST tree
        INPUTS:
          -prog: AST tree where to insert the parsed instruction
          -words: List of words to parse
          -nline: Number of the line that is beign parsed

        RETURNS:
          -True: Success. Instruction parsed and added into the AST
          -False: Not an instruction
          -An exception is raised in case of a sintax error
    """

    # -- Check if the first word is a correct nemonic
    if not words[0] in Instruction.opcodes.keys():
        msg = "ERROR: Unkwown instruction {} in line {}".format(words[0], nline)
        raise SyntaxError(msg, nline)

    # -- Check if it is a nenomic with no arguments (HALT, WAIT)
    if parse_instruction_arg0(prog, words, nline):
        return True

    # -- Check if it is a nenomic with 1 argument (LD, ST...)
    if parse_instruction_arg1(prog, words, nline):
        return True

    return False


def parse_line(prog, line,  nline):
    """Parse one line of the assembly program"""

    # - Split the line into words
    words = line.split()

    # -- Check if the line is an ORG directive
    if parse_org(prog, words, nline):
        return

    # -- check if the first word in the line is a label
    # -- If so, insert it into the symbol table
    if parse_label(prog, words[0], nline):
        words = words[1:]

        # -- Etiqueta sola
        if len(words) == 0:
            return

        # -- Comentarios
        if Lexer.is_comment(words[0]):
            return

    # -- Parse instructions
    if parse_instruction(prog, words, nline):
        return

    # --- Debug
    print ("[{}] {}".format(nline, words))


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

    # -- DEBUG: Show only the line with code
    print("\nPass 1:")
    for nline, line in enumerate(asmfile):

        # - Remove blank lines
        if Lexer.is_blank_line(line) or Lexer.is_comment_line(line):
            continue

        print("[{}] {}".format(nline+1, line))

    # -- Syntax analisis: line by line
    print("\nPass 2:")
    for nline, line in enumerate(asmfile):

        # - Remove blank lines
        if Lexer.is_blank_line(line) or Lexer.is_comment_line(line):
            continue

        # -- Parse line
        try:
            parse_line(prog, line, nline+1)

        # -- There was a syntax error. Print the message and exit
        except SyntaxError as e:
            print(e.msg)
            sys.exit()


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

    # -- Semantics analisis: Check if all the labels are ok
    # -- All the labels should have an address
    try:
        prog.assign_labels()

    except SyntaxError as e:
        print(e.msg)
        sys.exit()

    # -- Write the machine code in the output file file
    with open(OUTPUT_FILE, mode='w') as f:
        f.write(prog.machine_code())

    # -- Only in verbose mode
    if verbose:
        # -- Print the symbol table
        print()
        print("Symbol table:\n")
        for key in prog.symtable:
            print("{} = 0x{:02X}".format(key, prog.symtable[key]))

        # -- Print the parsed code
        print()
        print("SIMPLEZ assembly program:\n")
        print(prog)

        # -- Print the machine cod
        print()
        print("Machine code:\n")
        print(prog.machine_code())
