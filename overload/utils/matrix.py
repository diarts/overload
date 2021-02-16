from typing import List, Dict, Tuple, Union, Callable

from overload.type.type import _Type
from overload.exception.matrix import (
    ImplementationAlreadyRegistered,
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
            raise ImplementationAlreadyRegistered()

        # Add new column.
        new_imp_index = len(self.columns)
        self.columns.append(callable_)

        # Update rows.
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

    def find(self, args: List[_Type], kwargs: Dict[str, _Type]) -> Callable:
        """Find function in overload matrix by it arguments types.

        Returns:
            Callable: function who matched with arguments or default function.

        """
        # Check kwargs types.
        kwargs_imps = {index for index in range(len(self.rows[0]))}

        for arg, type_ in kwargs.items():
            # Get indexes of matched implementations.
            for index in kwargs_imps.copy():
                if self.rows[arg][index] != type_:
                    kwargs_imps.remove(index)

            # Not found implementation with current kwargs.
            if not kwargs_imps:
                raise ValueError

        # Found implementations with current kwargs. Check args types.
        args_imps = kwargs_imps

        # Get indexes of matched implementations.
        iter_args = iter(args)
        for arg, list_ in self.rows.items():
            # Kwargs type.
            if arg in kwargs:
                continue
            try:
                for index in args_imps.copy():
                    if list_[index] != next(iter_args):
                        args_imps.remove(index)
            except StopIteration:
                break

        if not args_imps:
            raise ImplementationNotFound(args=args, kwargs=kwargs)

        else:
            return self.implementation(tuple(args_imps)[0])
