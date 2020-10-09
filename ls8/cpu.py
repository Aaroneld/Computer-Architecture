"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        self.mem = [0] * 256 

        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)

        self.reg = [0] * 8

        self.pc = None
        self.ir = None
        self.mar = None 
        self.mdr = None
        self.fl = None 




    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # 00PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        program = open(program, 'r')

        instructions = program.readlines()

        for instruction in instructions:

                inst = instruction

                if '#' in inst:
                    inst = inst.split('#', 1)[0]

                if inst[0] != '#':

                    self.mem[address] = int(inst.strip('\n'), 2)
                    address += 1
                    
        
        

    def ram_read(self, address):

        return self.mem[address]
    
    def ram_write(self, address, value):

        self.mem[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            print(reg_a, reg_b)
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        self.pc = 0 
        self.ir = self.ram_read(self.pc)
        self.reg[6] = 245

        while running:

            if self.ir == 0b10000010: # if LDI
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
                self.pc += 3
            
            elif self.ir == 0b01000111: # if print reg
                print("print")
                print(self.reg[self.ram_read(self.pc + 1)])
                self.pc += 2 
            
            elif self.ir == 0b10100010: # if mult:
                self.alu(
                    "MUL", 
                    self.ram_read(self.pc + 1),
                    self.ram_read(self.pc + 2))

                self.pc += 3 

            elif self.ir == 0b00000001: # if halt 
                running = False  

            elif self.ir == 0b01000101: # if push
                self.ram_write(self.reg[6], self.reg[self.ram_read(self.pc + 1)])
                self.reg[6] -= 1 
                self.pc += 2
            
            elif self.ir == 0b01000110: #if pop
                self.reg[6] += 1
                self.reg[self.ram_read(self.pc + 1)] = self.mem[self.reg[6]]  
                self.pc += 2 

            else:
                print("Unreadable instruction")
                self.pc += 1 
            
            self.ir = self.ram_read(self.pc)
            





