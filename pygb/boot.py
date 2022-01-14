class Boot:

    def __init__(self, *, path):
        self._path = path
        self._content: bytes = b''

    def load_boot(self):
        with open(self._path, "rb") as boot_file:
            self._content = boot_file.read()

    def read_boot(self, *, address: int, size: int=1) -> bytes:
        return self._content[address: address + size]
