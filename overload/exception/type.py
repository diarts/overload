from typing import Any

from .base import OverloadException

__all__ = (
    'TypeException',
    'UnknownType',
    'CustomTypeError',
    'CustomTypeAlreadyExist',
    'IndexValueError',
    'SingleTypeError',
)


class TypeException(OverloadException):
    """Base overload lib exception for overload.type.type._TypeHandler
    exceptions."""
    __slots__ = ()

    _text = 'Base exception of type module.'
    _code = 100


class UnknownType(TypeException):
    """Exception raise if overload.type.type._TypeHandler
    catch unknown type."""
    __slots__ = ()

    _text = 'Unknown type was found: {type}'
    _code = 101

    def __init__(self, type_: Any):
        """
        Args:
            type_ (type): Founded unknown type.

        """
        super().__init__(self._text.format(type=type_))


class CustomTypeError(TypeException):
    """Exception raise if user try add not type key to __custom_types__ of
    overload.type.type._TypeHandler."""
    __slots__ = ()

    _text = 'Key must be an type type, current key {type} is {type} type.'
    _code = 102

    def __init__(self, type_: Any):
        """
        Args:
            type_ (Any): Transmitted type for add in __custom_types__.

        """
        super().__init__(self._text.format(type=type_))


class CustomTypeAlreadyExist(TypeException):
    """Exception raise if user try add custom type
    which already exist in __custom_types__."""
    __slots__ = ()

    _text = 'Type {type} already exist with index={index}.'
    _code = 103

    def __init__(self, type_: type, index: int):
        """
        Args:
            type_ (type): Type which user try add in __custom_types__.
            index (int): Index of exist type.

        """
        super().__init__(self._text.format(type=type_, index=index))


class IndexValueError(TypeException):
    """Exception raise if user try add new custom type with wrong index value
    to overload.type.type._TypeHandler."""
    __slots__ = ()

    _text = ('Index for new type must be integer more than 99 '
             'and not be already is use.')
    _code = 104


class SingleTypeError(TypeException):
    """Exception raise if in implementation annotations will found single type
    variable more than one time."""
    __slots__ = ()

    _text = (
        'In annotations will found more than one single type variable {type_}.'
    )
    _code = 105

    def __init__(self, type_: type):
        super().__init__(self._text.format(type=type_))
