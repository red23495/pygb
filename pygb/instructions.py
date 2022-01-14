from abc import abstractmethod
from typing import ClassVar, TYPE_CHECKING
if TYPE_CHECKING:
    from pygb.cpu import CPU


class Instruction:
    name = ''
    opcode = 0
    instructions = {}

    @classmethod
    def register(cls, val: ClassVar["Instruction"]):
        cls.instructions[val.opcode] = val()

    @classmethod
    def get_instruction(cls, opcode: int) -> "Instruction":
        inst = cls.instructions.get(opcode)
        if inst is None:
            raise Exception('No instruction with opcode {} is found'.format(opcode))
        return inst

    @abstractmethod
    def execute(self, cpu: "CPU"):
        raise Exception('Must override this function')


class NO_OP(Instruction):

    name = 'NO_OP'
    opcode = 0x0000

    def execute(self, cpu: "CPU"):
        pass


Instruction.register(NO_OP)
