from abc import abstractmethod
from typing import ClassVar, TYPE_CHECKING
if TYPE_CHECKING:
    from pygb.cpu import CPU


class Instruction:
    name = ''
    opcode = 0
    instructions = {}
    cycles = 4

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


class NO_OP(Instruction):

    name = 'NOP'
    opcode = 0x00
    cycles = 4

    def execute(self, cpu: "CPU"):
        pass


Instruction.register(NO_OP)


class LD_SP_D16(Instruction):
    name = 'LD_SP_D16'
    opcode = 0x31
    cycles = 12

    def execute(self, cpu: "CPU"):
        lsb: int = cpu.fetch_next()
        msb: int = cpu.fetch_next()
        cpu.reg_sp = (msb << 8) + lsb


Instruction.register(LD_SP_D16)
