from typing import Any, List
from abc import ABCMeta, abstractmethod

from overload.exception.overloader import (
    AnnotationCountError,
    ArgumentNameError,
    OverlappingError,
)
from overload.type.type import _TypeHandler
from overload.implementation.base import ABCImplementation
from overload.exception.overloader import MissedAnnotations


class ABCOverloader(metaclass=ABCMeta):
    """Base overload class. This class getting default object and register
    many implementations for it, based at their arguments types.
    When calling overloaded object, runned it implementation, who arguments
    types match with call arguments types.

    Class attributes:
        __implementation_class__ (Any): Wrapper class, for overload object
            implementations.

    Attributes:
        __type_handler__ (_TypeHandler): Annotation converting class.

    Args:
        overload_object (Any): Overload object.
        strict (bool): Activate validation of implementation annotations count
            and it priority compared overload object annotations.
        overlapping (bool): Activate registration of implementation with
            same annotations as the default overload object.
        deep (bool): Saving and validate implementation
            and object calling parameter not only on top level.

            Example saving annotations:
                (deep = False)
                var: dict[str, list[int]] -> var: dict
                (deep = True)
                var: dict[str, list[int]] -> var: dict[str, list[int]]

            Example converting calling parameter:
                (deep = False)
                {'var': [1,2,3]} -> dict
                (deep = True)
                {'var':[1,2,3]} -> dict[str, list[int]]

    """
    __slots__ = (
        '_default',
        '_varieties',
        '_strict',
        '_overlapping',
        '__type_handler__',
    )

    __implementation_class__: Any = ABCImplementation
    __type_handler__: _TypeHandler

    _varieties: List[Any]
    _strict: bool
    _overlapping: bool

    def __init__(
            self,
            overload_object: Any,
            strict: bool = False,
            overlapping: bool = False,
    ):
        self.__type_handler__ = _TypeHandler()
        self._strict = strict
        self._overlapping = overlapping
        self._varieties = []

        self._register_implementation(overload_object)
        self._default = self.varieties[-1]

    def __repr__(self):
        return "<class 'Overloader'>"

    @property
    def is_strict(self):
        """Validate 'typed args' count in register implementation is mapped
        with count of 'typed args' in default object."""
        return self._strict

    @property
    def default(self) -> __implementation_class__:
        """Default object, who was overload."""
        return self._default

    @property
    def varieties(self):
        """Contain all implementations of overload object."""
        return self._varieties

    @property
    def can_overlapping(self) -> bool:
        """If it is True, overloader can storage implementation with
        same annotations as the default overload object.
        """
        return self._overlapping

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

        if not self.can_overlapping:
            new_annotations = self.__type_handler__.converting_annotations(
                annotations=object_.__annotations__,
            )

            for parameter, value in new_annotations.items():
                if value != self.default.__annotations__[parameter]:
                    break
            else:
                raise OverlappingError()
