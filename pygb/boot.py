class Boot:

    def __init__(self, *, path):
        self._path = path
        self._content: bytes = ''

    def load_boot(self):
        with open(self._path, "rb") as boot_file:
            self._content = boot_file.read()
        
    def read_boot(self, address: int):
        return self._content[address]
