import pytest

from overload.type.type import _TypeHandler

from .data import out_up_types_types_and_expectations


@pytest.mark.type
@pytest.mark.parametrize(
    'input_type,expected',
    out_up_types_types_and_expectations,
)
def test_out_up_types(input_type, expected):
    handler = _TypeHandler()
    type_ = handler.out_up_types(input_type)
    assert type_ == expected
