from pygb.boot import Boot
from pygb.cart import Cart
from pygb.vram import VRAM
from pygb.io import IO


class Bus:

    ENTRY_POINT = 0x0100
    SWITHCABLE_BANK_START = 0x4000
    VRAM_START = 0x8000
    EXRAM_START = 0xA000
    IO_START = 0xFF00
    HRAM_START = 0xFF80

    def __init__(self, *, boot: Boot, vram: VRAM, cart: Cart, io: IO):
        self._boot_enabled = boot is not None
        self._boot = boot
        self._vram = vram
        self._cart = cart
        self._io = io

    def read(self, *, address: int, size: int=1) -> bytearray:
        if address < self.ENTRY_POINT and self._boot_enabled:
            return self._read_from_boot(address=address, size=size)
        if address < self.SWITHCABLE_BANK_START:
            return self._read_from_cart(address=address, size=size)
        if self.VRAM_START <= address < self.EXRAM_START:
            return self._read_from_vram(address=address, size=size)
        if self.IO_START <= address < self.HRAM_START:
            return self._read_from_io(address=address, size=size)
        raise Exception(f'0x{address:04X} is not A Valid Address')

    def _read_from_boot(self, *, address: int, size: int) -> bytearray:
        return self._boot.read_boot(address=address, size=size)

    def _read_from_cart(self, *, address: int, size: int) -> bytearray:
        return self._cart.read(address=address, size=size)

    def _read_from_vram(self, *, address: int, size: int) -> bytearray:
        return self._vram.read(address=address - self.VRAM_START, size=size)

    def _write_to_vram(self, *, address: int, value: bytes):
        self._vram.write(address=address - self.VRAM_START, value=value)

    def _read_from_io(self, *, address: int, size: int) -> bytearray:
        return self._io.read(address=address - self.IO_START, size=size)

    def _write_to_io(self, *, address: int, value: bytes):
        self._io.write(address=address - self.IO_START, value=value)

    def write(self, *, address: int, value: bytes):
        if self.VRAM_START <= address < self.EXRAM_START:
            return self._write_to_vram(address=address, value=value)
        if self.IO_START <= address < self.HRAM_START:
            return self._write_to_io(address=address, value=value)
        raise Exception(f'Write to 0x{address:04X} is not allowed' )
