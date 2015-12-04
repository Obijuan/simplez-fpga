# import sasm


class Test_progs(object):
    """Program example 1: adding two numbes"""
    SIMPLEZ1 = [0x0, 0x205, 0x406, 0x007, 0xE00, 0x007, 0x008, 0x00]

    """Programa ejemplo 2: Pueba de BR"""
    SIMPLEZ2 = [0X0, 0x205, 0x406, 0x007, 0x601, 0x007, 0x008, 0x00]


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
        self.state = self.INIT

    def decode(self, inst):
        """Return the opcode and argument of a given instruction in machine code"""
        return (inst >> 9, inst & 0x1FF)

    def show(self):
        print("PC = {:03X}".format(self._PC))
        print("A = {:03X}".format(self._A))
        print("Z = {}".format(self._Z))
        if self.state == self.STOPED:
            print("Micro stopped! Halt executed")
        else:
            # - Fetch the current instruction
            ir = self._mem[self._PC]

            # - Print the current instruction
            print("Next: [{:03X}] {}".format(self._PC, self.code2asm(ir)))

    def load(self, prog):
        """Load a program into the memory. The program consist of a list of consecutive
           instructions"""

        l = len(prog)
        s._mem[0:l] = prog

    def mem(self, nblocks=32):
        """Print the memory
           nblocks = number of blocks (of 16 words) to print"""
        print("       0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F")
        for block in range(nblocks):
            linecode = ""
            for pos in self._mem[(block * 16):(block*16 + 16)]:
                linecode += "{:03X} ".format(pos)

            print("[{:03X}] {}".format(block*16, linecode))

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

    def step(self):
        """Simulate the next instruction"""

        if self.state == self.STOPED:
            print("Micro stopped! Halt executed")
            return

        elif self.state == self.INIT:
            print("Initial state:")
            self.show()
            print()
            self.state = self.RUNNING

        # - Fetch the current instruction
        ir = self._mem[self._PC]

        # - Print the current instruction
        print("Executing: [{:03X}] {}".format(self._PC, self.code2asm(ir)))

        # - Point to the next instruction
        self._PC += 1

        # - Decode the instruction
        opcode, addr = self.decode(ir)

        # - Decode de extended instructions
        xopcode = ir >> 8

        # - Execute
        self._execute(opcode, addr, xopcode)

        # - Update the Z flag
        if self._A == 0:
            self._Z = 1
        else:
            self._Z = 0

        self.show()

    def code2asm(self, inst):
        """Return a string with the given machine code instruction in assembly language"""

        opcode, addr = self.decode(inst)
        nemonic = self.NEMONIC[opcode]
        asm = "{}".format(nemonic)

        # - Add the argument
        if nemonic in ["ST", "LD", "ADD", "BR", "BZ"]:
            asm += " /H'{:03X}".format(addr)

        # - Add the content of the memory (as a comment)
        if nemonic in ["ST", "LD", "ADD"]:
            asm += ";  [{:03X}]={:03X}".format(addr, self._mem[addr])

        return asm


if __name__ == "__main__":
    """Main program"""

    s = simplez()

    # - Load a simple program
    s.load(Test_progs.SIMPLEZ2)

    # - s.step()
