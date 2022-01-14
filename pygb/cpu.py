from pygb.instructions import Instruction
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygb.motherboard import Motherboard


class CPU:

    def __init__(self, *, motherboard: "Motherboard"):
        self._motherboard = motherboard
        self.reg_pc = 0x0000

    def _fetch_instruction(self) -> Instruction:
        opcode = self._motherboard.read(address=self.reg_pc, size=1)[0]
        self.reg_pc += 1
        return Instruction.get_instruction(opcode)

    def execute(self):
        raise Exception('Not Implemented Yet')

    def tick(self):
        instruction: Instruction = self._fetch_instruction()
        instruction.execute(self)

