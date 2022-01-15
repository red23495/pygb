class Cart:

    def __init__(self):
        self._content: bytearray = bytearray()

    def read(self, *, address: int, size: int=1):
        return self._content[address: address+size]
