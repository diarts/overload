from typing import List, Dict, Tuple, Union, Callable

from overload.type.type import _Type
from overload.exception.matrix import (
    ImplementationError,
    ImplementationIndexError,
    ImplementationNotFound,
)


class _OverloadMatrix:
    """Class of matrix with headers for arguments and implementation.
    Matrix value can be only is overload.type.type._Type class.

    Matrix Format:
                        imp_1           imp_2       imp_3
        arg_1   |       _Type      |    _Type   |   None    |
        arg_2   |       None       |    _Type   |   _Type   |
        arg_3   |   (_Type, _Type) |    None    |   _Type   |

    """
    __slots__ = ('_arguments', '_implementations')

    def __repr__(self) -> str:
        return "<class 'MatrixTable'>"

    def __str__(self) -> str:
        return (f'Matrix with contained {len(self.columns)} implementations '
                f'and {len(self.rows)} args.')

    def __init__(self):
        self._implementations = []
        self._arguments = {}

    @property
    def columns(self) -> list:
        """List of callable implementations."""
        return self._implementations

    @property
    def rows(self) -> dict:
        """Dict of arguments types for each implementation."""
        return self._arguments

    def __setitem__(self, callable_: Callable,
                    args: Dict[str, List[Union[_Type, Tuple[_Type, ...]]]]):
        """Add new implementation to matrix and it arguments types.

        Args:
            callable_ (Callable): New implementation who
                must add to matrix columns.
            args (dict): Dict with arguments types of new implementation.

        """
        if callable_ in self.columns:
            raise ImplementationError()

        # add new column
        new_imp_index = len(self.columns)
        self.columns.append(callable_)

        # update rows
        for arg, types in args.items():
            try:
                self.rows[arg].append(types)
            except KeyError:
                self.rows[arg] = [None for _ in range(new_imp_index)]
                self.rows[arg].append(types)

        for arg, types in self.rows.items():
            if len(types) < new_imp_index + 1:
                types.append(None)

    def implementation(self, imp_id: int) -> Callable:
        """Get matrix contain implementation by it id."""
        try:
            return self.columns[imp_id]
        except IndexError:
            if imp_id is not int or imp_id < 0:
                raise ImplementationIndexError(type(imp_id), imp_id)
            else:
                raise ImplementationNotFound(imp_id)
