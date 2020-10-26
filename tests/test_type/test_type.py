import pytest

from overload.type.type import _TypeHandler
from overload.exception.type import UnknownType

from .data import (
    out_up_types_types_and_expectations,
    set_custom_type_index,
)


@pytest.mark.type
def test_get_type_index():
    handler = _TypeHandler()

    class TestUnknownType:
        pass

    with pytest.raises(UnknownType):
        handler[TestUnknownType]


@pytest.mark.type
@pytest.mark.parametrize(
    'exception,type_,index',
    set_custom_type_index,
)
def test_set_custom_type_index(exception, type_, index):
    handler = _TypeHandler()

    if exception:
        with pytest.raises(exception):
            handler[type_] = index
    else:
        new_index = handler[type_] = index
        assert new_index == index
        assert new_index == handler[type_]


@pytest.mark.type
@pytest.mark.parametrize(
    'input_type,expected',
    out_up_types_types_and_expectations,
)
def test_out_up_types(input_type, expected):
    handler = _TypeHandler()
    type_ = handler.out_up_types(input_type)
    assert type_ == expected
