"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        # The MAR contains the address that is being read or written to.
        self.mar = 0
        # The MDR contains the data that was read or the data to write
        self.mdr = 0

    def ram_read(self, address):
        value_in_memory = self.ram[address]
        # SETS MAR TO THE ADDRESS BEING READ
        self.set_mar(address)
        # SETS MDR TO THE VALUE STORED IN MEMORY
        self.set_mdr(value_in_memory)
        return value_in_memory

    def ram_write(self, address, value):
        self.ram[address] = value
        # SETS MAR TO THE ADDRESS BEING WRITTEN
        self.set_mar(address)
        # SETS MDR TO THE VALUE BEING WRITTEN
        self.set_mdr(value)
        return self.ram[address]

    def set_mar(self, address):
        self.mar = address

    def set_mdr(self, value):
        self.mdr = value

    def load(self):
        """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        """Load instructions from a file"""
        starting_memory = 0
        # debug = 1
        file_name = sys.argv[1]
        with open(file_name) as f:
            for line in f:
                # WE DIVIDE LINE IF THERE IS A COMMENT
                comment_split = line.split('#')
                # WE TAKE THE LEFT PART OF THE ARRAY, AND STRIP SPACE AT THE END
                instruction = comment_split[0].strip()
                # print(f'Instruction: {instruction} in line {debug}')
                # WE CONVERT STRING WITH BINARY CODE INTO BINARY VALUE
                binary_code = int(instruction, 2)
                # WE SAVE EACH INSTRUCTION INTO RAM
                self.ram_write(starting_memory, binary_code)
                # WE INCREMENT THE ADDRESS IN MEMORE SO WE CAN ADD THE NEXT INSTRUCTION IN THE NEXT SLOT
                starting_memory += 1
                # debug += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010

        running = True

        while running:
            # INSTRUCTION REGISTER
            IR = self.ram_read(self.pc)
            # GET THE NEXT 2 BYTES OF DATA IN CASE WE NEED THEM
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            inc_size = 0
            # LDI
            if IR == LDI:
                self.reg[operand_a] = operand_b
                inc_size = 3
            # PRN
            elif IR == PRN:
                value = self.reg[operand_a]
                print(value)
                inc_size = 2
            # HLT
            elif IR == HLT:
                print("Operations halted.")
                sys.exit(-1)
                running = False
            # INSTRUCTION NOT RECOGNISED
            else:
                print("Invalid instruction")
                running = False

            self.pc += inc_size
