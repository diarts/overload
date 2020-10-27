from typing import Any
from abc import ABCMeta, abstractmethod

from overload.type.type import _TypeHandler


class Overloader(metaclass=ABCMeta):
    """Base overload class. This class getting default object and register
    many implementations for it, based at their arguments types.
    When calling overloaded object, runned it implementation, who arguments
    types match with call arguments types."""

    __slots__ = ('_default', '_varieties', '__dict__',)

    __type_handler__ = _TypeHandler

    _strict = False
    _default_type_count = 0

    def __init__(self, overload_object: Any, strict: bool = False):
        self.default = overload_object
        self._strict = strict
        self._varieties = []
        self.__type_handler__ = self.__type_handler__()

    def __repr__(self):
        return '<Overload class>'

    @property
    def is_strict(self):
        """Check 'typed args' count in register implementation is mapped with
        count of 'typed args' in default object."""
        return self._strict

    @property
    def default(self) -> Any:
        """Default object, who was overload."""
        return self._default

    @default.setter
    def default(self, obj: Any):
        """Register new implementation of overload object as default
        implementation."""
        self._default = obj

    @property
    def varieties(self):
        return self._varieties

    @abstractmethod
    def register(self, obj: Any):
        """Register new implementation of overload object
        by it argument types."""
        pass
