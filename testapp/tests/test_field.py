import uuid
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from prefix_id.field import PrefixIDField
from testapp.models import MyModel


@pytest.mark.parametrize(
    "prefix,expected_prefix,max_length",
    [
        ("my_prefix", "my_prefix", 32),
        ("", None, 22),
        (None, None, 22),
    ],
)
@patch("prefix_id.field.models.CharField.__init__")
def test_field__valid_prefix__calls_super_init_with_correct_params(
    mock_charfield_init, prefix, expected_prefix, max_length
):
    field = PrefixIDField(prefix=prefix)

    mock_charfield_init.assert_called_once()
    assert mock_charfield_init.call_args.kwargs["max_length"] == max_length
    assert mock_charfield_init.call_args.kwargs["editable"] is False
    assert mock_charfield_init.call_args.kwargs["unique"] is True
    assert field.prefix == expected_prefix


@pytest.mark.parametrize(
    "prefix,expected_prefix,length",
    [
        ("my_prefix", "my_prefix_", 32),
        ("", "", 22),
        (None, "", 22),
    ],
)
def test_field__valid_prefix__get_default_works_correctly(prefix, expected_prefix, length):
    field = PrefixIDField(prefix=prefix)

    with patch("prefix_id.base62.uuid.uuid4", return_value=uuid.UUID("ed0af078-8d87-4f09-9081-2b2f6b07aaa3")):
        default = field.get_default()

    assert default.startswith(expected_prefix)
    assert len(default) == length


@pytest.mark.parametrize(
    "prefix,expected_prefix,length",
    [
        ("my_prefix", "my_prefix", 32),
        ("", None, 22),
        (None, None, 22),
    ],
)
def test_field__valid_prefix__deconstruct_works_correctly(prefix, expected_prefix, length):
    field = PrefixIDField(prefix=prefix)

    with patch("prefix_id.base62.uuid.uuid4", return_value=uuid.UUID("ed0af078-8d87-4f09-9081-2b2f6b07aaa3")):
        values = field.deconstruct()

    assert values[3] == {"max_length": length, "unique": True, "editable": False, "prefix": expected_prefix}


@pytest.mark.parametrize(
    "value,expectation",
    [
        ("test_model_525msfids", does_not_raise()),
        ("wrong_prefix_353mfmefw", pytest.raises(ValidationError)),
        ("353mfmefw", pytest.raises(ValidationError)),
        ("", pytest.raises(ValidationError)),
        (None, pytest.raises(ValidationError)),
        (1.1, pytest.raises(ValidationError)),
    ],
)
def test_field__with_prefix__works_or_raises_validationerror_appropriately(value, expectation):
    instance = MyModel()
    field = instance._meta.get_field("id")

    with expectation:
        field.validate(value, instance)


@pytest.mark.parametrize(
    "value,expectation",
    [
        ("353mfmefw", does_not_raise()),
        ("has_prefix_353mfmefw", pytest.raises(ValidationError)),
        ("", pytest.raises(ValidationError)),
        (None, pytest.raises(ValidationError)),
        (1.1, pytest.raises(ValidationError)),
    ],
)
def test_field__without_prefix__works_or_raises_validationerror_appropriately(value, expectation):
    instance = MyModel()
    field = instance._meta.get_field("id_no_prefix")

    with expectation:
        field.validate(value, instance)


@pytest.mark.parametrize(
    "value,expectation",
    [
        ("353mfmefw", does_not_raise()),
        ("has_prefix_353mfmefw", pytest.raises(ValidationError)),
        ("", does_not_raise()),
        (None, pytest.raises(ValidationError)),
        (1.1, pytest.raises(ValidationError)),
    ],
)
def test_field__with_prefix_allow_blank__works_or_raises_validationerror_appropriately(value, expectation):
    instance = MyModel()
    field = instance._meta.get_field("id_no_prefix_blank")

    with expectation:
        field.validate(value, instance)


@pytest.mark.parametrize(
    "value,expectation",
    [
        ("353mfmefw", does_not_raise()),
        ("has_prefix_353mfmefw", pytest.raises(ValidationError)),
        ("", pytest.raises(ValidationError)),
        (None, does_not_raise()),
        (1.1, pytest.raises(ValidationError)),
    ],
)
def test_field__with_prefix_allow_none__works_or_raises_validationerror_appropriately(value, expectation):
    instance = MyModel()
    field = instance._meta.get_field("id_no_prefix_none")

    with expectation:
        field.validate(value, instance)
