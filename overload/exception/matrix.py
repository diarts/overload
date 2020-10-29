from typing import Any

from .base import OverloadException

__all__ = (
    'MatrixError',
    'ImplementationError',
    'ImplementationIndexError',
    'ImplementationNotFound',
)


class MatrixError(OverloadException):
    """Base exception of all matrix errors."""

    __slots__ = ()

    _text = 'Base exception of matrix util.'
    _code = 300


class ImplementationError(MatrixError):
    """Raise when add implementation already contain in matrix."""

    __slots__ = ()

    _text = ("Error of add implementation to matrix: "
             "this implementation already contain in matrix.")
    _code = 301


class ImplementationIndexError(MatrixError):
    """Raise when getting implementation id has wrong type."""

    __slots__ = ()

    _text = (
        'Implementation index must be an positive integer, not {type}={value}.'
    )
    _code = 302

    def __init__(self, type_: type, value: Any):
        super().__init__(self._text.format(type=type_, value=value))


class ImplementationNotFound(MatrixError):
    """Raise when getting implementation id not contained in matrix."""

    __slots__ = ()

    _text = 'Implementation with id={id} not contain in matrix.'
    _code = 303

    def __init__(self, id_: int):
        super().__init__(self._text.format(id=id_))
