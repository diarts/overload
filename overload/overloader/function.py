from collections.abc import Callable

from .base import Overloader
from overload.exception.overloader import (
    FunctionRegisterTypeError,
    MissedAnnotations,
    AnnotationCountError,
)

__all__ = (
    'FunctionOverloader',
)


class FunctionOverloader(Overloader):
    """Class function overloading. It take function and registering
    implementations of it. After that it storage this implementations
    and dispatch calls base it arguments types."""
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        self._validate_register_obj(function_)
        self.default = function_

    def register(self, obj: Callable) -> None:
        """Register new implementation of function/coroutine."""
        self._validate_register_obj(obj)
        self._varieties.append(obj)

    def _validate_register_obj(self, obj: Callable) -> None:
        """Validation of registering object."""
        if not isinstance(obj, Callable):
            raise FunctionRegisterTypeError()
        if not hasattr(obj, '__annotations__'):
            raise MissedAnnotations()
        if self.is_strict:
            if len(obj.__annotations__) > self._default_type_count:
                raise AnnotationCountError()
