"""File contain base implementation class."""
from abc import ABCMeta, abstractmethod
from typing import Dict, Any

from overload.type.type import _Type

__all__ = ()


class ABCImplementation(metaclass=ABCMeta):
    """Base overload object implementation class.

    Attrs:
        _implementation (Any): Storage implementation of overload object.
        _overload (Any): Overload object.
        __annotations__ (Dict[str, _Type]): Unique set of implementation
            parameters types.

    Args:
        implementation (Any): Storage implementation of overload object.
        overload (Any): Overload object.

    """
    __slots__ = ('_implementation', '_strict', '__annotations__')

    def __init__(self, implementation: Any, annotations: Dict[str, _Type],
                 strict: bool = False) -> None:
        self.__annotations__: Dict[str, _Type] = annotations
        self._implementation = implementation
        self._strict = strict

    @property
    def implementation(self) -> Any:
        """Storage implementation of overload object."""
        return self._implementation

    def __repr__(self) -> str:
        return f'< Implementation class > annotations={self.__annotations__}.'

    def __str__(self) -> str:
        return f'Implementation of {self.implementation}'

    def __eq__(self, other) -> bool:
        if isinstance(other, ABCImplementation):
            return self.__annotations__ == other.__annotations__
        else:
            raise TypeError(
                'Implementation object can be compare only with other '
                f'Implementation object, not {type(other)}.'
            )

    def __call__(self, *args, **kwargs) -> Any:
        return self.implementation(*args, **kwargs)

    @abstractmethod
    def compare(self, *args, **kwargs) -> bool:
        """Comparing parameters with storage annotations."""
        ...
