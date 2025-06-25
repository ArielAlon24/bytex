# Structure

Like [Pydantic](https://github.com/pydantic/pydantic), but for binary formats.

## Installation

> (Still not available on PyPI)

```console
$ pip install structure
```

## Example

Let’s say you want to represent a user profile in your application using a compact binary format.

Start by defining the user type as a `StructureEnum`:

```python
from structure import StructureEnum
from structure.types import U8
from enum import auto


class UserType(StructureEnum(U8)):
    """
    An enum representing a UserType in a single byte.
    """
    ADMIN = auto()
    MEMBER = auto()
    GUEST = auto()
```

> A `StructureEnum` is just a subclass of Python's built-in `Enum`, so you can use it as you normally would.

Then define a structure for a date:

```python
from structure import Structure
from structure.types import U16, U8


class Date(Structure):
    year: U16
    month: U8
    day: U8
```

Now bring it all together into a `UserProfile` structure:

```python
from structure import Structure
from structure.length_encodings import Terminator
from typing import Annotated


class UserProfile(Structure):
    user_type: UserType
    joined_at: Date
    name: Annotated[str, Terminator("\0")]
```

> The `Annotated[str, Terminator("\0")]` represents a string with a `Terminator` length encoding, meaning the string is serialized with a `"\0"` at the end, and deserialized until a `"\0"` is encountered (There is a pre-made type for this exact scenario called `CStr` located at `structure.types`, which is a null-terminated string).

And you're done!

You can now serialize and parse binary data with ease:

```python
from structure import Endianes

profile = UserProfile(
    user_type=UserType.ADMIN,
    joined_at=Date(year=2024, month=6, day=25),
    name="admin"
)

binary: bytes = profile.dump(endianes=Endianes.LITTLE)
parsed: UserProfile = UserProfile.parse(binary, endianes=Endianes.LITTLE)
```
