from .base import OverloadException

__all__ = (
    'TypeException',
    'UnknownType',
)


class TypeException(OverloadException):
    """Base overload lib exception for overload.type.type._TypeHandler
    exceptions."""
    pass


class UnknownType(TypeException):
    """Exception raise if overload.type.type._TypeHandler
    catch unknown type."""

    _text = 'Unknown type was found: {type}'

    def __init__(self, type_: type):
        """
        Args:
            type_ (type): Founded unknown type.

        """
        super().__init__(self._text.format(type=type_))
