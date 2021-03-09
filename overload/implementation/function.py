"""File contain function implementation class."""
from typing import Union, Dict, List, Tuple
from collections import deque

from overload.type.type import _Type

from .base import ABCImplementation

__all__ = (
    'FunctionImplementation',
)


class FunctionImplementation(ABCImplementation):
    """Implementation for overload function."""

    def compare(
            self,
            named: Dict[str, Union[_Type]] = None,
            unnamed: Union[List[_Type], Tuple[_Type, ...]] = None,
    ) -> bool:
        """Comparing kwargs parameters and args with storage annotations.

        Args:
            named (dict): Dict with format {parameter_name : type}.
            unnamed (list or tuple): Parameters passed without key.
                Sequence of type.

        """
        named = named or {}
        unnamed = unnamed or ()

        check_annotations = self.__annotations__.copy()

        # Compare named parameters.
        for parameter, type_ in named.items():
            try:
                if type_ != check_annotations.pop(parameter):
                    return False
            except KeyError:
                if self._strict:
                    return False
                else:
                    continue

        check_annotations = deque(check_annotations.values())

        # Compare unnamed parameters.
        try:
            for type_ in unnamed:
                if type_ != check_annotations.popleft():
                    return False
        except IndexError:
            return False if self._strict else True
        else:
            return True
