from pygb.instructions import Instruction
from pygb.utils import is_bit_set, set_bit
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygb.motherboard import Motherboard


class CPU:

    def __init__(self, *, motherboard: "Motherboard"):
        self._motherboard = motherboard
        self._reg_a = 0x00
        self._reg_b = 0x00
        self._reg_c = 0x00
        self._reg_d = 0x00
        self._reg_e = 0x00
        self._reg_f = 0x00
        self._reg_h = 0x00
        self._reg_l = 0x00
        self._reg_pc = 0x0000
        self._reg_sp = 0x0000

    @property
    def reg_a(self):
        return self._reg_a

    @reg_a.setter
    def reg_a(self, value):
        self._reg_a = value & 0xFF

    @property
    def reg_b(self):
        return self._reg_b

    @reg_b.setter
    def reg_b(self, value):
        self._reg_b = value & 0xFF

    @property
    def reg_c(self):
        return self._reg_c

    @reg_c.setter
    def reg_c(self, value):
        self._reg_c = value & 0xFF

    @property
    def reg_d(self):
        return self._reg_d

    @reg_d.setter
    def reg_d(self, value):
        self._reg_d = value & 0xFF

    @property
    def reg_e(self):
        return self._reg_a

    @reg_e.setter
    def reg_e(self, value):
        self._reg_e = value & 0xFF

    @property
    def reg_f(self):
        return self._reg_f

    @reg_f.setter
    def reg_f(self, value):
        self._reg_f = value & 0xFF

    @property
    def reg_h(self):
        return self._reg_h

    @reg_h.setter
    def reg_h(self, value):
        self._reg_h = value & 0xFF

    @property
    def reg_l(self):
        return self._reg_l

    @reg_l.setter
    def reg_l(self, value):
        self._reg_l = value & 0xFF

    @property
    def reg_pc(self):
        return self._reg_pc

    @reg_pc.setter
    def reg_pc(self, value):
        self._reg_pc = value & 0xFFFF

    @property
    def reg_sp(self):
        return self._reg_sp

    @reg_sp.setter
    def reg_sp(self, value):
        self._reg_sp = value & 0xFFFF

    @property
    def reg_af(self):
        return (self.reg_a << 8) | self.reg_f

    @reg_af.setter
    def reg_af(self, val: int):
        self.reg_a = (val >> 8)
        self.reg_f = (val & 0xFF)

    @property
    def reg_bc(self):
        return (self.reg_b << 8) | self.reg_c

    @reg_bc.setter
    def reg_bc(self, val: int):
        self.reg_b = (val >> 8)
        self.reg_c = (val & 0xFF)

    @property
    def reg_de(self):
        return (self.reg_d << 8) | self.reg_e

    @reg_de.setter
    def reg_de(self, val: int):
        self.reg_d = (val >> 8)
        self.reg_e = (val & 0xFF)

    @property
    def reg_hl(self):
        return (self.reg_h << 8) | self.reg_l

    @reg_hl.setter
    def reg_hl(self, val: int):
        self.reg_h = (val >> 8)
        self.reg_l = (val & 0xFF)

    @staticmethod
    def unset_bit(source: int, bit_no: int):
        source &= ~(0x1 << bit_no)
        return source

    @property
    def flag_z(self):
        return is_bit_set(self.reg_f, 7)

    @flag_z.setter
    def flag_z(self, val):
        self.reg_f = set_bit(self.reg_f, 7) if val else CPU.unset_bit(self.reg_f, 7)

    @property
    def flag_n(self):
        return is_bit_set(self.reg_f, 6)

    @flag_n.setter
    def flag_n(self, val):
        self.reg_f = set_bit(self.reg_f, 6) if val else CPU.unset_bit(self.reg_f, 6)

    @property
    def flag_h(self):
        return is_bit_set(self.reg_f, 5)

    @flag_h.setter
    def flag_h(self, val):
        self.reg_f = set_bit(self.reg_f, 5) if val else CPU.unset_bit(self.reg_f, 5)

    @property
    def flag_c(self):
        return is_bit_set(self.reg_f, 4)

    @flag_c.setter
    def flag_c(self, val):
        self.reg_f = set_bit(self.reg_f, 4) if val else CPU.unset_bit(self.reg_f, 4)

    def read(self, *, address: int, size: int=1):
        return self._motherboard.read(address=address, size=size)

    def write(self, *, address: int, value: bytes):
        self._motherboard.write(address=address, value=value)

    def fetch_next(self) -> int:
        opcode = self.read(address=self.reg_pc, size=1)[0]
        self.reg_pc += 1
        return opcode

    def _fetch_instruction(self) -> Instruction:
        opcode = self.fetch_next()
        return Instruction.get_instruction(opcode)

    def tick(self):
        instruction: Instruction = self._fetch_instruction()
        instruction.init(self)
        instruction.execute(self)
        instruction.set_flags(self)
        self._motherboard.tick(cycles=instruction.cycles)
        print(f'{instruction.name}: A={self.reg_a:02X} B={self.reg_b:02X} C={self.reg_c:02X} HL={self.reg_hl:04X} SP={self.reg_sp:04X}, PC={self.reg_pc:04X}, cycles={self._motherboard._ticks}, flags={self.reg_f:08b}')

