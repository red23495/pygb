from pygb.boot import Boot
from pygb.bus import Bus
from pygb.cpu import CPU
from pygb.vram import VRAM
from pygb.cart import Cart
from pygb.io import IO
from pygb.apu import APU

class Motherboard:

    def __init__(self):
        self._boot = Boot(path='boot/dmg_boot.bin')
        self._boot.load_boot()
        self._vram = VRAM()
        self._cart = Cart()
        self._io = IO(onupdate=self.io_update_handler)
        self._bus = Bus(boot=self._boot, vram=self._vram, cart=self._cart, io=self._io)
        self._cpu = CPU(motherboard=self)
        self._apu = APU()
        self._ticks = 0

    def io_update_handler(self, address: int, value: bytes):
        address = address + 0xFF00
        if address == 0xFF11:  # nr11 channel 1 wave pattern
            self._apu.nr11 = value
            return
        if address == 0xFF12:  # nr12 channel 1 envelop
            self._apu.nr12 = value
            return
        if address == 0xFF24:  # nr50 output channel control
            self._apu.nr50 = value
            return
        if address == 0xFF25:  # nr51 output terminal selection
            self._apu.nr51 = value
            return
        if address == 0xFF26:  # nr52 sound on/off
            self._apu.nr52 = value
            return
        raise Exception(f'Unknown IO Register 0x{address:04X}')

    def read(self, *, address: int, size: int=1):
        return self._bus.read(address=address, size=size)

    def write(self, *, address: int, value: bytes):
        self._bus.write(address=address, value=value)

    def tick(self, *, cycles: int):
        self._ticks += cycles

    def run(self):
        while True:
            self._cpu.tick()

    def close(self):
        self._apu.close()
