from pygb.instructions import Instruction
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygb.motherboard import Motherboard


class CPU:

    def __init__(self, *, motherboard: "Motherboard"):
        self._motherboard = motherboard
        self.reg_a = 0x00
        self.reg_b = 0x00
        self.reg_c = 0x00
        self.reg_d = 0x00
        self.reg_e = 0x00
        self.reg_f = 0x00
        self.reg_h = 0x00
        self.reg_l = 0x00
        self.reg_pc = 0x0000
        self.reg_sp = 0x0000

    @property
    def reg_af(self):
        return (self.reg_a << 8) & self.reg_f

    @reg_af.setter
    def reg_af(self, val: int):
        self.reg_a = (val >> 8)
        self.reg_f = (val & 0xFF)

    @property
    def reg_bc(self):
        return (self.reg_b << 8) & self.reg_c

    @reg_bc.setter
    def reg_bc(self, val: int):
        self.reg_b = (val >> 8)
        self.reg_c = (val & 0xFF)

    @property
    def reg_de(self):
        return (self.reg_d << 8) & self.reg_e

    @reg_de.setter
    def reg_de(self, val: int):
        self.reg_d = (val >> 8)
        self.reg_e = (val & 0xFF)

    @property
    def reg_hl(self):
        return (self.reg_h << 8) & self.reg_l

    @reg_hl.setter
    def reg_hl(self, val: int):
        self.reg_h = (val >> 8)
        self.reg_l = (val & 0xFF)

    @staticmethod
    def is_bit_set(val: int, bit_no: int):
        return bool((val >> bit_no) & 0x01)

    @staticmethod
    def set_bit(source: int, bit_no: int):
        source |= (0x1 << bit_no)
        return source

    @staticmethod
    def unset_bit(source: int, bit_no: int):
        source &= ~(0x1 << bit_no)
        return source

    @property
    def flag_z(self):
        return CPU.is_bit_set(self.reg_f, 7)

    @flag_z.setter
    def flag_z(self, val):
        self.reg_f = CPU.set_bit(self.reg_f, 7) if val else CPU.unset_bit(self.reg_f, 7)

    @property
    def flag_n(self):
        return CPU.is_bit_set(self.reg_f, 6)

    @flag_n.setter
    def flag_n(self, val):
        self.reg_f = CPU.set_bit(self.reg_f, 6) if val else CPU.unset_bit(self.reg_f, 6)

    @property
    def flag_h(self):
        return CPU.is_bit_set(self.reg_f, 5)

    @flag_h.setter
    def flag_h(self, val):
        self.reg_f = CPU.set_bit(self.reg_f, 5) if val else CPU.unset_bit(self.reg_f, 5)

    @property
    def flag_c(self):
        return CPU.is_bit_set(self.reg_f, 4)

    @flag_c.setter
    def flag_c(self, val):
        self.reg_f = CPU.set_bit(self.reg_f, 4) if val else CPU.unset_bit(self.reg_f, 4)

    def fetch_next(self) -> int:
        opcode = self._motherboard.read(address=self.reg_pc, size=1)[0]
        self.reg_pc += 1
        return opcode

    def _fetch_instruction(self) -> Instruction:
        opcode = self.fetch_next()
        return Instruction.get_instruction(opcode)

    def tick(self):
        instruction: Instruction = self._fetch_instruction()
        instruction.execute(self)
        instruction.set_flags(self)
        self._motherboard.tick(cycles=instruction.cycles)
        print(f'{instruction.name}: A={self.reg_a} SP={self.reg_sp}, PC={self.reg_pc}, cycles={self._motherboard._ticks}, flags={self.reg_f:08b}')

