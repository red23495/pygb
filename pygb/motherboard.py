from pygb.boot import Boot
from pygb.bus import Bus
from pygb.cpu import CPU


class Motherboard:

    def __init__(self):
        self._boot = Boot(path='boot/dmg_boot.bin')
        self._boot.load_boot()
        self._bus = Bus(boot=self._boot)
        self._cpu = CPU(motherboard=self)

    def read(self, *, address: int, size: int=1):
        return self._bus.read(address=address, size=size)

    def run(self):
        while True:
            self._cpu.tick()
