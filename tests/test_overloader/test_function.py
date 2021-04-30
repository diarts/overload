import pytest

from overload.overloader.function import FunctionOverloader

from .data import FUNCTION_OVERLOADER_REGISTER


@pytest.mark.overloader
@pytest.mark.parametrize(
    'default,strict,overlap,new_func,exception',
    FUNCTION_OVERLOADER_REGISTER,
)
def test_validation_of_register_func(default, strict, overlap, new_func,
                                     exception):
    overloader = FunctionOverloader(default, strict, overlap)

    if exception:
        with pytest.raises(exception):
            overloader._validate_register_object(new_func)
    else:
        assert not overloader._validate_register_object(new_func)
