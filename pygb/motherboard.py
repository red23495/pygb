from pygb.boot import Boot
from pygb.bus import Bus
from pygb.cpu import CPU
from pygb.vram import VRAM
from pygb.cart import Cart


class Motherboard:

    def __init__(self):
        self._boot = Boot(path='boot/dmg_boot.bin')
        self._boot.load_boot()
        self._vram = VRAM()
        self._cart = Cart()
        self._bus = Bus(boot=self._boot, vram=self._vram, cart=self._cart)
        self._cpu = CPU(motherboard=self)
        self._ticks = 0

    def read(self, *, address: int, size: int=1):
        return self._bus.read(address=address, size=size)

    def write(self, *, address: int, value: bytes):
        self._bus.write(address=address, value=value)

    def tick(self, *, cycles: int):
        self._ticks += cycles

    def run(self):
        while True:
            self._cpu.tick()
