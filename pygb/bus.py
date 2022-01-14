from pygb.boot import Boot

class Bus:

    def __init__(self, *, boot: Boot):
        self._boot_enabled = boot is not None
        self._boot = boot

    def read(self, address):
        raise Exception('Not Implemented Yet')

    def write(self, address, value):
        raise Exception('Not Implemented Yet')