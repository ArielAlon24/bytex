import pytest

from bytex.bits import BitBuffer, Bits
from bytex.endianes import Endianes
from bytex.errors import AlignmentError, InsufficientDataError


@pytest.mark.parametrize(
    "bits, endianes, expected_bytes",
    [
        (
            [True, False, True, False, True, False, True, False],
            Endianes.BIG,
            bytes([0b10101010]),
        ),
        (
            [True, False, True, False, True, False, True, False],
            Endianes.LITTLE,
            bytes([0b10101010]),
        ),
        ([True] * 8, Endianes.BIG, bytes([0xFF])),
        ([True] * 8, Endianes.LITTLE, bytes([0xFF])),
        ([False] * 8, Endianes.BIG, bytes([0x00])),
        ([False] * 8, Endianes.LITTLE, bytes([0x00])),
        ([True, False] * 8, Endianes.BIG, bytes([0b10101010, 0b10101010])),
        ([True, False] * 8, Endianes.LITTLE, bytes([0b10101010, 0b10101010])),
    ],
)
def test_to_bytes(bits: Bits, endianes: Endianes, expected_bytes: bytes):
    buffer = BitBuffer()
    buffer.write(bits)
    data = buffer.to_bytes(endianes)
    assert data == expected_bytes, f"{data.hex()} != {expected_bytes.hex()}"


@pytest.mark.parametrize(
    "data, endianes, expected_bits",
    [
        (
            bytes([0b10101010]),
            Endianes.BIG,
            [True, False, True, False, True, False, True, False],
        ),
        (
            bytes([0b10101010]),
            Endianes.LITTLE,
            [True, False, True, False, True, False, True, False],
        ),
        (bytes([0xFF]), Endianes.BIG, [True] * 8),
        (bytes([0x00]), Endianes.LITTLE, [False] * 8),
        (
            bytes([0b11001100]),
            Endianes.BIG,
            [True, True, False, False, True, True, False, False],
        ),
        (
            bytes([0b11001100]),
            Endianes.LITTLE,
            [True, True, False, False, True, True, False, False],
        ),
    ],
)
def test_from_bytes(data: bytes, endianes: Endianes, expected_bits: Bits):
    buffer = BitBuffer.from_bytes(data, endianes)
    bits = buffer.read(len(expected_bits))
    assert (
        bits == expected_bits
    ), f"{_bits_to_string(bits)} != {_bits_to_string(expected_bits)}"


@pytest.mark.parametrize(
    "input_bits, read_count, expected_read, remaining_bits",
    [
        ([True, False, True], 1, [True], [False, True]),
        ([False, True], 2, [False, True], []),
        ([True] * 10, 5, [True] * 5, [True] * 5),
    ],
)
def test_read(
    input_bits: Bits, read_count: int, expected_read: Bits, remaining_bits: Bits
):
    buffer = BitBuffer()
    buffer.write(input_bits)

    assert buffer.read(read_count) == expected_read
    assert buffer.read(len(input_bits) - read_count) == remaining_bits


@pytest.mark.parametrize("bits", [[True] * 7, [False] * 3, [True, False] * 5])
def test_to_bytes_raises_on_unaligned(bits: Bits):
    buffer = BitBuffer()
    buffer.write(bits)
    if len(bits) % 8 != 0:
        with pytest.raises(AlignmentError, match="Bit buffer is not aligned"):
            buffer.to_bytes(Endianes.BIG)


@pytest.mark.parametrize(
    "initial_bits, read_count",
    [
        ([], 1),
        ([True], 2),
        ([False] * 4, 5),
    ],
)
def test_read_too_many_bits(initial_bits: Bits, read_count: int):
    buffer = BitBuffer()
    buffer.write(initial_bits)
    with pytest.raises(InsufficientDataError):
        buffer.read(read_count)


def _bits_to_string(bits: Bits) -> str:
    return "".join("1" if bit else "0" for bit in bits)
