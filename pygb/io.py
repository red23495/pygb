class IO:

    def __init__(self, *, onupdate):
        self._memory: bytearray = bytearray([0] * (0xFF80 - 0xFF00))
        self._update_handler = onupdate

    def read(self, *, address: int, size: int=1) -> bytearray:
        return self._memory[address: address + size]

    def write(self, *, address: int, value: bytes):
        current_address = address
        for byte in value:
            self._memory[current_address] = byte
            self._update_handler(address, byte)
            current_address += 1
