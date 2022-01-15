from abc import abstractmethod
from pygb.utils import is_bit_set
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

    def init(self, cpu: "CPU"):
        pass

    @abstractmethod
    def execute(self, cpu: "CPU"):
        pass

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


class LD_C_D8(Instruction):
    name = 'LD_C_D8'
    opcode = 0x0E
    cycles = 8

    def execute(self, cpu: "CPU"):
        cpu.reg_c = cpu.fetch_next()


Instruction.register(LD_C_D8)


class LD_DE_D16(Instruction):
    name = 'LD_DE_D16'
    opcode = 0x11
    cycles = 12

    def execute(self, cpu: "CPU"):
        lsb: int = cpu.fetch_next()
        msb: int = cpu.fetch_next()
        cpu.reg_de = (msb << 8) + lsb


Instruction.register(LD_DE_D16)


class LD_E_D8(Instruction):
    name = 'LD_E_D8'
    opcode = 0x1E
    cycles = 8

    def execute(self, cpu: "CPU"):
        cpu.reg_e = cpu.fetch_next()


Instruction.register(LD_E_D8)


class JR_NZ_R8(Instruction):
    name = 'JR_NZ_R8'
    opcode = 0x20

    def __init__(self):
        self._cycles = 8

    @property
    def cycles(self):
        return self._cycles

    def execute(self, cpu: "CPU"):
        offset = cpu.fetch_next()
        if not cpu.flag_z:
            cpu.reg_pc += offset
            self._cycles = 12
        else:
            self._cycles = 8


Instruction.register(JR_NZ_R8)


class LD_HL_D16(Instruction):
    name = 'LD_HL_D16'
    opcode = 0x21
    cycles = 12

    def execute(self, cpu: "CPU"):
        lsb: int = cpu.fetch_next()
        msb: int = cpu.fetch_next()
        cpu.reg_hl = (msb << 8) + lsb


Instruction.register(LD_HL_D16)


class LD_L_D8(Instruction):
    name = 'LD_C_D8'
    opcode = 0x2E
    cycles = 8

    def execute(self, cpu: "CPU"):
        cpu.reg_l = cpu.fetch_next()


Instruction.register(LD_L_D8)


class LD_SP_D16(Instruction):
    name = 'LD_SP_D16'
    opcode = 0x31
    cycles = 12

    def execute(self, cpu: "CPU"):
        lsb: int = cpu.fetch_next()
        msb: int = cpu.fetch_next()
        cpu.reg_sp = (msb << 8) + lsb


Instruction.register(LD_SP_D16)


class LD_HL_DEC_A(Instruction):
    name = 'LD_(HL-)_A'
    opcode = 0x32
    cycles = 8

    def execute(self, cpu: "CPU"):
        cpu.write(address=cpu.reg_hl, value=cpu.reg_a.to_bytes(1, 'big'))
        cpu.reg_hl -= 1


Instruction.register(LD_HL_DEC_A)


class LD_A_D8(Instruction):
    name = 'LD_A_D8'
    opcode = 0x3E
    cycles = 8

    def execute(self, cpu: "CPU"):
        cpu.reg_a = cpu.fetch_next()


Instruction.register(LD_A_D8)


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


class CB_PREFIX(Instruction):
    instructions = {}
    opcode = 0xCB

    @property
    def name(self):
        return self.instruction.name

    @property
    def cycles(self):
        return self.instruction.cycles

    def __init__(self):
        self.instruction: Instruction = None

    def init(self, cpu: "CPU"):
        sub_opcode = cpu.fetch_next()
        self.instruction = CB_PREFIX.get_instruction(sub_opcode)

    def execute(self, cpu: "CPU"):
        return self.instruction.execute(cpu)


class BIT_7H(Instruction):
    name = 'BIT_7H'
    opcode = 0x7C
    cycles = 8

    def set_z_flag(self, cpu: "CPU"):
        cpu.flag_z = 1 if is_bit_set(cpu.reg_h, 7) else 0


CB_PREFIX.register(BIT_7H)


Instruction.register(CB_PREFIX)
