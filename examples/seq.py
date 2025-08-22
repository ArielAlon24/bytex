from typing import Annotated, List

from bytex import Structure
from bytex.endianes import Endianes
from bytex.length_encodings import Exact, Fixed, Prefix
from bytex.types import U8, U32


class Sequences(Structure):
    up_to_ten_numbers: Annotated[List[U8], Fixed(10)]
    text: Annotated[str, Prefix(U32)]
    four_bytes: Annotated[bytes, Exact(4)]


def main() -> None:
    sequences = Sequences(
        up_to_ten_numbers=[1, 2],
        text="This can be 0xFFFF characters long!",
        four_bytes=b"\x01\x02\x03\x04",
    )
    print(sequences)

    data = sequences.dump(endianes=Endianes.LITTLE)
    print(f"Dumped length: {len(data)}")

    roundtrip = Sequences.parse(data, endianes=Endianes.LITTLE)
    print(roundtrip)

    assert roundtrip.text == sequences.text
    assert roundtrip.four_bytes == sequences.four_bytes

    # `Exact` fills left out values with the default value (in this case 0)
    original_length = len(sequences.up_to_ten_numbers)
    assert roundtrip.up_to_ten_numbers[:original_length] == sequences.up_to_ten_numbers
    assert all(value == 0 for value in roundtrip.up_to_ten_numbers[original_length:])


if __name__ == "__main__":
    main()
