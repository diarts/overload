import pytest

from overload.type.type import _TypeHandler

from .data import (
    OUT_UP_TYPES_AND_EXPECTATIONS,
    CONVERTING_ARGS,
    CONVERTING_KWARGS,
)

set_custom_type_handler = _TypeHandler()


@pytest.mark.type
@pytest.mark.parametrize(
    'deep,input_type,expected',
    OUT_UP_TYPES_AND_EXPECTATIONS,
)
def test_out_up_types(deep, input_type, expected):
    handler = _TypeHandler()
    type_ = handler.out_up_types(input_type)
    assert type_ == expected


@pytest.mark.type
@pytest.mark.parametrize(
    'args,result',
    CONVERTING_ARGS,
)
def test_converting_args(args, result):
    handler = _TypeHandler()
    assert result == handler.converting_args(args)


@pytest.mark.type
@pytest.mark.parametrize(
    'kwargs,result',
    CONVERTING_KWARGS,
)
def test_converting_args(kwargs, result):
    handler = _TypeHandler()
    assert result == handler.converting_kwargs(kwargs)
