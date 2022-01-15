from abc import abstractmethod
from typing import ClassVar, TYPE_CHECKING
if TYPE_CHECKING:
    from pygb.cpu import CPU


class Instruction:
    name = ''
    opcode = 0
    instructions = {}
    cycles = 4
    z_flag = None
    n_flag = None
    h_flag = None
    c_flag = None

    @classmethod
    def register(cls, val: ClassVar["Instruction"]):
        cls.instructions[val.opcode] = val()

    @classmethod
    def get_instruction(cls, opcode: int) -> "Instruction":
        inst = cls.instructions.get(opcode)
        if inst is None:
            raise Exception('No instruction with opcode 0x{:02X} is found'.format(opcode))
        return inst

    @abstractmethod
    def execute(self, cpu: "CPU"):
        raise Exception('Must override this function')

    def set_z_flag(self, cpu: "CPU"):
        if self.z_flag:
            cpu.reg_f = self.z_flag

    def set_n_flag(self, cpu: "CPU"):
        if self.n_flag:
            cpu.reg_f = self.n_flag

    def set_h_flag(self, cpu: "CPU"):
        if self.h_flag:
            cpu.reg_f = self.h_flag

    def set_c_flag(self, cpu: "CPU"):
        if self.c_flag:
            cpu.reg_f = self.c_flag

    def set_flags(self, cpu: "CPU"):
        self.set_z_flag(cpu)
        self.set_n_flag(cpu)
        self.set_h_flag(cpu)
        self.set_c_flag(cpu)


class NO_OP(Instruction):

    name = 'NOP'
    opcode = 0x00
    cycles = 4

    def execute(self, cpu: "CPU"):
        pass


Instruction.register(NO_OP)


class LD_BC_D16(Instruction):
    name = 'LD_BC_D16'
    opcode = 0x01
    cycles = 12

    def execute(self, cpu: "CPU"):
        lsb: int = cpu.fetch_next()
        msb: int = cpu.fetch_next()
        cpu.reg_bc = (msb << 8) + lsb


Instruction.register(LD_BC_D16)


class LD_DE_D16(Instruction):
    name = 'LD_DE_D16'
    opcode = 0x11
    cycles = 12

    def execute(self, cpu: "CPU"):
        lsb: int = cpu.fetch_next()
        msb: int = cpu.fetch_next()
        cpu.reg_de = (msb << 8) + lsb


Instruction.register(LD_DE_D16)


class LD_HL_D16(Instruction):
    name = 'LD_HL_D16'
    opcode = 0x21
    cycles = 12

    def execute(self, cpu: "CPU"):
        lsb: int = cpu.fetch_next()
        msb: int = cpu.fetch_next()
        cpu.reg_hl = (msb << 8) + lsb


Instruction.register(LD_HL_D16)


class LD_SP_D16(Instruction):
    name = 'LD_SP_D16'
    opcode = 0x31
    cycles = 12

    def execute(self, cpu: "CPU"):
        lsb: int = cpu.fetch_next()
        msb: int = cpu.fetch_next()
        cpu.reg_sp = (msb << 8) + lsb


Instruction.register(LD_SP_D16)


class XOR_A(Instruction):
    name = 'XOR_A'
    opcode = 0xAF
    cycles = 4
    n_flag = 0
    h_flag = 0
    c_flag = 0

    def set_z_flag(self, cpu: "CPU"):
        cpu.flag_z = int(cpu.reg_a == 0)

    def execute(self, cpu: "CPU"):
        cpu.reg_a ^= cpu.reg_a


Instruction.register(XOR_A)
