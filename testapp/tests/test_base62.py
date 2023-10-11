import uuid
from unittest.mock import patch

import pytest

from prefix_id.base62 import encode, generate_base62_id


@pytest.mark.parametrize(
    "value,expected",
    [
        (uuid.UUID("00000000-0000-0000-0000-000000000000"), "0"),
        (uuid.UUID("ed0af078-8d87-4f09-9081-2b2f6b07aaa3"), "7dibcWPErBrFmkZFgLHFHZ"),
        ("ed0af078-8d87-4f09-9081-2b2f6b07aaa3", "7dibcWPErBrFmkZFgLHFHZ"),
    ],
)
def test_encode__with_valid_uuid__encodes_correctly(value, expected):
    encoded_str = encode(value)

    assert isinstance(encoded_str, str)
    assert len(encoded_str) <= 22
    assert encoded_str == expected


@pytest.mark.parametrize(
    "value",
    [
        "invalid",
        0.43,
    ],
)
def test_encode__with_invalid_input__raises_valueerror(value):
    with pytest.raises(ValueError):
        encode(value)


@patch("prefix_id.base62.encode")
def test_generate_base62_id__calls_encode(mock_encode):
    generate_base62_id()

    mock_encode.assert_called_once()
