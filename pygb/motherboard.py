from pygb import boot
from pygb.boot import Boot


from pygb.boot import Boot
from pygb.bus import Bus

class Motherboard:

    def __init__(self):
        self._boot = Boot(path='boot/dmg_boot.bin')
        self._boot.load_boot()
        self._bus = Bus(boot=self._boot)
        # add ram
        # add cpu