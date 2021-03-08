import pytest

from overload.type.type import _TypeHandler

from .data import (
    out_up_types_types_and_expectations,
)

set_custom_type_handler = _TypeHandler()


@pytest.mark.type
@pytest.mark.parametrize(
    'deep,input_type,expected',
    out_up_types_types_and_expectations,
)
def test_out_up_types(deep, input_type, expected):
    handler = _TypeHandler(deep=deep)
    type_ = handler.out_up_types(input_type)
    assert type_ == expected
