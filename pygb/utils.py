def is_bit_set(val: int, bit_no: int):
    return bool((val >> bit_no) & 0x01)


def set_bit(source: int, bit_no: int):
    source |= (0x1 << bit_no)
    return source
