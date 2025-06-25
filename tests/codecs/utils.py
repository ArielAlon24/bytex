from bytex.bits import Bits


def bits_to_string(bits: Bits) -> str:
    return "".join([str(int(i)) for i in bits])


def string_to_bits(string: str) -> Bits:
    return [bool(int(i)) for i in string]
