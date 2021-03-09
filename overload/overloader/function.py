from types import FunctionType
from collections.abc import Callable

from overload.overloader.base import ABCOverloader
from overload.exception.overloader import (
    FunctionRegisterTypeError,
)
from overload.implementation.function import FunctionImplementation

__all__ = (
    'FunctionABCOverloader',
)


class FunctionABCOverloader(ABCOverloader):
    """Class function overloading. It take function and registering
    implementations of it. After that it storage this implementations
    and dispatch calls base it arguments types."""
    __slots__ = ()

    __implementation_class__ = FunctionImplementation

    def __init__(self, overload_function: Callable, *args, **kwargs):
        super().__init__(overload_function, *args, **kwargs)

    def __repr__(self):
        return ("<class 'FunctionOverloader'>"
                f' implementation count = {len(self.varieties)}.')

    def __str__(self):
        return f'Overloader for function {self.default}.'

    def __call__(self, *args, **kwargs):
        return self.default(*args, **kwargs)

    def register(self, function_: Callable) -> None:
        """Register new implementation of function/coroutine."""
        super(FunctionABCOverloader, self).register(function_)

    def _validate_register_object(self, function_: Callable) -> None:
        """Validation of registering object."""
        if type(function_) is not FunctionType:
            raise FunctionRegisterTypeError()

        super(FunctionABCOverloader, self)._validate_register_object(function_)
