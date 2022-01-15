class VRAM:

    def __init__(self):
        self._memory: bytearray = bytearray([0] * (0xA000 - 0x8000))

    def read(self, *, address: int, size: int=1) -> bytearray:
        return self._memory[address: address + size]

    def write(self, *, address: int, value: bytes):
        current_address = address
        for byte in value:
            self._memory[current_address] = byte
            current_address += 1
