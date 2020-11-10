import pytest

from overload.type.type import _TypeHandler
from overload.exception.type import UnknownType

from .data import (
    out_up_types_types_and_expectations,
    set_custom_type_index,
    mapping_type,
)

set_custom_type_handler = _TypeHandler()


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
    if exception:
        with pytest.raises(exception):
            set_custom_type_handler[type_] = index
    else:
        new_index = set_custom_type_handler[type_] = index
        assert new_index == index
        assert new_index == set_custom_type_handler[type_]


@pytest.mark.type
@pytest.mark.parametrize(
    'deep,input_type,expected',
    out_up_types_types_and_expectations,
)
def test_out_up_types(deep, input_type, expected):
    handler = _TypeHandler(deep=deep)
    type_ = handler.out_up_types(input_type)
    assert type_ == expected


@pytest.mark.type
@pytest.mark.parametrize(
    'type_,add_unknown,exception,mapped_type',
    mapping_type,
)
def test_mapping_type(type_, add_unknown, exception, mapped_type):
    handler = _TypeHandler(deep=True)

    type_ = handler.out_up_types(type_)

    if exception:
        with pytest.raises(exception):
            handler._mapping_type(type_)

    else:
        res = handler._mapping_type(type_, add_unknown)
        assert mapped_type == res
