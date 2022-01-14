from pygb.boot import Boot


class Bus:

    ENTRY_POINT = 0x0100

    def __init__(self, *, boot: Boot):
        self._boot_enabled = boot is not None
        self._boot = boot

    def read(self, *, address: int, size: int=1) -> bytes:
        if address < self.ENTRY_POINT and self._boot_enabled:
            return self._read_from_boot(address=address, size=size)
        raise Exception('Not A Valid Address')

    def _read_from_boot(self, *, address: int, size: int):
        return self._boot.read_boot(address=address, size=size)

    def write(self, address, value):
        raise Exception('Not Implemented Yet')
