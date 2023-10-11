import typing
import uuid

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE62_LENGTH = len(BASE62)


def encode(value: typing.Union[uuid.UUID, str]) -> str:
    if isinstance(value, str):
        try:
            value = uuid.UUID(value)
        except ValueError:
            raise ValueError("Base62 encoding requires a UUID value")
    elif not isinstance(value, uuid.UUID):
        raise ValueError("Base62 encoding requires a UUID value")

    value = value.int
    if value == 0:
        return BASE62[0]

    arr = []
    while value:
        value, rem = divmod(value, BASE62_LENGTH)
        arr.append(BASE62[rem])

    arr.reverse()
    return "".join(arr)


def generate_base62_id() -> str:
    return encode(uuid.uuid4())
