from unittest.mock import call, patch

from testapp.models import MyModel


@patch("prefix_id.field.generate_base62_id")
def test_model__calls_generate(mock_generate):
    mock_generate.return_value = "5wefww4tsd"
    MyModel()

    mock_generate.assert_has_calls([call(), call(), call(), call()])
