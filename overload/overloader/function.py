from typing import Tuple, Dict
from types import FunctionType
from collections.abc import Callable

from overload.overloader.base import ABCOverloader
from overload.type.type import _Type
from overload.exception.overloader import (
    FunctionRegisterTypeError,
    AnnotationCountError,
    MissedAnnotations,
)
from overload.implementation.function import FunctionImplementation

__all__ = (
    'FunctionOverloader',
)


class FunctionOverloader(ABCOverloader):
    """Class function overloading. It take function and registering
    implementations of it. After that it storage this implementations
    and dispatch calls base it arguments types."""
    __slots__ = ()

    __implementation_class__ = FunctionImplementation

    def __init__(self, overload_function: Callable, *args, **kwargs):
        super().__init__(overload_function, *args, **kwargs)

    def __repr__(self):
        return (f"< Overloaded function {self.__origin_name__} >"
                f' implementation count = {len(self.varieties)}.')

    def __str__(self):
        return f'< Overloaded "{self.__origin_name__}" >'

    def __call__(self, *args, **kwargs):
        args_types = self.__type_handler__.converting_args(args)
        kwargs_types = self.__type_handler__.converting_kwargs(kwargs)
        implementation = self._get_variety(args_types, kwargs_types)
        return implementation(*args, **kwargs)

    def register(self, function_: FunctionType) -> None:
        """Registering new implementation of function/coroutine."""
        super(FunctionOverloader, self).register(function_)

    def _validate_register_object(self, function_: FunctionType) -> None:
        """Validation of registering object."""
        if type(function_) is not FunctionType:
            raise FunctionRegisterTypeError()

        arg_count = function_.__code__.co_argcount
        kw_count = function_.__code__.co_kwonlyargcount

        if not function_.__annotations__ and arg_count + kw_count:
            raise MissedAnnotations()
        elif len(function_.__annotations__) < arg_count + kw_count:
            raise AnnotationCountError()

        super(FunctionOverloader, self)._validate_register_object(function_)

    def _get_variety(
            self, args: Tuple[_Type, ...], kwargs: Dict[str, _Type],
    ) -> Callable:
        """Get compared function implementation."""
        if args or kwargs:
            for implementation in reversed(self.varieties):
                if implementation.compare(named=kwargs, unnamed=args):
                    return implementation
        else:
            for implementation in self.varieties[::-1]:
                if not implementation.__all_annotations__:
                    return implementation

        return self.default
