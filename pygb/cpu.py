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

    @property
    def reg_bc(self):
        return (self.reg_b << 8) & self.reg_c

    @property
    def reg_de(self):
        return (self.reg_d << 8) & self.reg_e

    @property
    def reg_hl(self):
        return (self.reg_h << 8) & self.reg_l

    def fetch_next(self) -> int:
        opcode = self._motherboard.read(address=self.reg_pc, size=1)[0]
        self.reg_pc += 1
        return opcode

    def _fetch_instruction(self) -> Instruction:
        opcode = self.fetch_next()
        return Instruction.get_instruction(opcode)

    def execute(self):
        raise Exception('Not Implemented Yet')

    def tick(self):
        instruction: Instruction = self._fetch_instruction()
        instruction.execute(self)
        self._motherboard.tick(cycles=instruction.cycles)
        print(f'{instruction.name}: SP={self.reg_sp}, PC={self.reg_pc}, cycles={self._motherboard._ticks}')

