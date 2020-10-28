from collections.abc import Callable

from .base import Overloader
from overload.exception.overloader import (
    FunctionRegisterTypeError,
    MissedAnnotations,
    AnnotationCountError,
    ArgumentNameError,
)

__all__ = (
    'FunctionOverloader',
)


def _function_for_getting_type():
    pass


class FunctionOverloader(Overloader):
    """Class function overloading. It take function and registering
    implementations of it. After that it storage this implementations
    and dispatch calls base it arguments types."""
    __slots__ = ()

    __function_type__ = type(_function_for_getting_type)

    def __init__(self, overload_function: Callable, strict: bool = False):
        super().__init__(overload_function, strict)

    def __repr__(self):
        return ('<Function Overload class> '
                f'implementation count = {len(self.varieties)}.')

    def __str__(self):
        return 'Function/coroutine overloading class.'

    def __call__(self, *args, **kwargs):
        return self.default(*args, **kwargs)

    def as_default(self, function_: Callable):
        """Register new implementation of overload object as default
        implementation."""
        self._validate_register_func(function_)
        self.default = function_

    def register(self, function_: Callable) -> None:
        """Register new implementation of function/coroutine."""
        self._validate_register_func(function_)
        self._varieties.append(function_)

    def _validate_register_func(self, function_: Callable) -> None:
        """Validation of registering object."""
        if type(function_) is not self.__function_type__:
            raise FunctionRegisterTypeError()

        if not function_.__annotations__:
            raise MissedAnnotations()

        if self.is_strict:
            ann_count = len(function_.__annotations__)
            def_ann_count = len(self.default.__annotations__)

            if ann_count != def_ann_count:
                raise AnnotationCountError()

            default_ann_keys = tuple(self.default.__annotations__.keys())
            for index, value in enumerate(function_.__annotations__):
                if value != default_ann_keys[index]:
                    raise ArgumentNameError()
