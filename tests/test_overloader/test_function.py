import pytest

from overload.overloader.function import FunctionOverloader

from .data import validation_of_register_func


@pytest.mark.overloader
@pytest.mark.parametrize(
    'default,strict,new_func,exception',
    validation_of_register_func,
)
def test_validation_of_register_func(default, strict, new_func, exception):
    overloader = FunctionOverloader(default, strict)

    with pytest.raises(exception):
        overloader._validate_register_object(new_func)
