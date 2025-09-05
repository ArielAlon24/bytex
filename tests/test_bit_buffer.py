import pytest

from bytex.bits import BitBuffer, Bits, bits_to_string, string_to_bits
from bytex.errors import AlignmentError, InsufficientDataError


@pytest.mark.parametrize(
    "bits, expected_bytes",
    [
        (string_to_bits("10101010"), bytes([0b10101010])),
        (string_to_bits("11111111"), bytes([0xFF])),
        (string_to_bits("00000000"), bytes([0x00])),
        (string_to_bits("10101010" * 2), bytes([0b10101010, 0b10101010])),
    ],
)
def test_to_bytes(bits: Bits, expected_bytes: bytes) -> None:
    buffer = BitBuffer()
    buffer.write(bits)

    data = buffer.to_bytes()

    assert data == expected_bytes, f"{data.hex()} != {expected_bytes.hex()}"


@pytest.mark.parametrize(
    "data, expected_bits",
    [
        (bytes([0b10101010]), string_to_bits("10101010")),
        (bytes([0xFF]), string_to_bits("11111111")),
        (bytes([0x00]), string_to_bits("00000000")),
        (bytes([0b11001100]), string_to_bits("11001100")),
    ],
)
def test_from_bytes(data: bytes, expected_bits: Bits) -> None:
    buffer = BitBuffer.from_bytes(data)

    bits = buffer.read(len(expected_bits))

    assert (
        bits == expected_bits
    ), f"{bits_to_string(bits)} != {bits_to_string(expected_bits)}"


@pytest.mark.parametrize(
    "input_bits, read_count, expected_read, remaining_bits",
    [
        (string_to_bits("101"), 1, string_to_bits("1"), string_to_bits("01")),
        (string_to_bits("01"), 2, string_to_bits("01"), []),
        (string_to_bits("1" * 10), 5, [True] * 5, [True] * 5),
    ],
)
def test_read(
    input_bits: Bits, read_count: int, expected_read: Bits, remaining_bits: Bits
) -> None:
    buffer = BitBuffer()
    buffer.write(input_bits)

    assert buffer.read(read_count) == expected_read
    assert buffer.read(len(input_bits) - read_count) == remaining_bits


@pytest.mark.parametrize(
    "bits", [string_to_bits("1" * 7), string_to_bits("0" * 3), string_to_bits("10" * 5)]
)
def test_to_bytes_raises_on_unaligned(bits: Bits) -> None:
    buffer = BitBuffer()
    buffer.write(bits)

    if len(bits) % 8 != 0:
        with pytest.raises(AlignmentError):
            buffer.to_bytes()


@pytest.mark.parametrize(
    "initial_bits, read_count",
    [
        ([], 1),
        (string_to_bits("1"), 2),
        (string_to_bits("0" * 4), 5),
    ],
)
def test_read_too_many_bits(initial_bits: Bits, read_count: int) -> None:
    buffer = BitBuffer()
    buffer.write(initial_bits)

    with pytest.raises(InsufficientDataError):
        buffer.read(read_count)
