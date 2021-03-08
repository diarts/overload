from typing import Any, Callable
from abc import ABCMeta, abstractmethod

from overload.exception.overloader import (
    AnnotationCountError,
    ArgumentNameError,
)
from overload.type.type import _TypeHandler
from overload.implementation.base import ABSImplementation
from overload.exception.overloader import MissedAnnotations


class Overloader(metaclass=ABCMeta):
    """Base overload class. This class getting default object and register
    many implementations for it, based at their arguments types.
    When calling overloaded object, runned it implementation, who arguments
    types match with call arguments types."""

    __slots__ = ('_default', '_varieties', '__dict__',)

    __type_handler__ = _TypeHandler
    __implementation_class__ = ABSImplementation

    _strict = False

    def __init__(self, overload_object: Any, strict: bool = False):
        self._strict = strict
        self.__type_handler__ = self.__type_handler__()

        self._register_implementation(overload_object)
        self._default = self.varieties[-1]

    def __repr__(self):
        return "<class 'Overloader'>"

    @property
    def is_strict(self):
        """Check 'typed args' count in register implementation is mapped with
        count of 'typed args' in default object."""
        return self._strict

    @property
    def default(self) -> Callable:
        """Default object, who was overload."""
        return self._default

    @property
    def varieties(self):
        return self._varieties

    @abstractmethod
    def register(self, object_: Any):
        """Register new implementation of overload object
        by it argument types."""
        self._validate_register_object(object_)
        self._register_implementation(object_)

    def as_default(self, object_: Any):
        """Register new implementation of overload object as default
        implementation."""
        self.register(object_)
        self._default = self.varieties[-1]

    def _register_implementation(self, implementation: Any) -> None:
        """Registering new implementation of overload object."""
        new_implementation = self.__implementation_class__(
            implementation=implementation,
            annotations=self.__type_handler__.converting_annotations(
                annotations=implementation.__annotations__,
            ),
            strict=self._strict,
        )
        self._varieties.append(new_implementation)

    def _validate_register_object(self, object_: Any) -> None:
        """Validation of registering object."""
        if not getattr(object_, '__annotations__'):
            raise MissedAnnotations()

        if self.is_strict:
            ann_count = len(object_.__annotations__)
            def_ann_count = len(self.default.__annotations__)

            if ann_count != def_ann_count:
                raise AnnotationCountError()

            default_ann_keys = tuple(self.default.__annotations__.keys())
            for index, value in enumerate(object_.__annotations__):
                if value != default_ann_keys[index]:
                    raise ArgumentNameError()
