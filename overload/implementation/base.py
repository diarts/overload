"""File contain base implementation class."""
from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Dict, Any

from overload.type.type import _Type

__all__ = (
    'ABCImplementation',
)


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
    __slots__ = (
        '_implementation',
    )

    def __init__(
            self, implementation: Any, annotations: Dict[str, _Type],
        ) -> None:
        self._separate_annotations(implementation, annotations)
        self._implementation = implementation

    @property
    def implementation(self) -> Any:
        """Storage implementation of overload object."""
        return self._implementation

    @property
    @abstractmethod
    def __all_annotations__(self) -> Dict[str, _Type]:
        """Return all implementation annotations."""
        ...

    @abstractmethod
    def compare(self, *args, **kwargs) -> bool:
        """Comparing parameters with storage annotations."""
        ...

    @abstractmethod
    def _separate_annotations(self, implementation: Any,
                              annotations: Dict[str, _Type]) -> None:
        """Separate implementation annotations."""
        ...

    def __repr__(self) -> str:
        return (
            f'< Implementation class > annotations={self.__all_annotations__}.'
        )

    def __str__(self) -> str:
        return f'Implementation of {self.implementation}'

    def __eq__(self, other) -> bool:
        if isinstance(other, ABCImplementation):
            return self.__all_annotations__ == other.__all_annotations__
        else:
            raise TypeError(
                'Implementation object can be compare only with other '
                f'Implementation object, not {type(other)}.'
            )

    def __call__(self, *args, **kwargs) -> Any:
        return self.implementation(*args, **kwargs)
