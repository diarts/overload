from .base import OverloadException

__all__ = (
    'OverloaderError',
    'RegisterTypeError',
    'FunctionRegisterTypeError',
    'MissedAnnotations',
    'AnnotationCountError',
)


class OverloaderError(OverloadException):
    """Base overload lib exception for overload.overloader.base.Overload and
    it implementations exceptions."""

    __slots__ = ()

    _text = 'Base exception of overloader module.'
    _code = 200


class RegisterTypeError(OverloaderError):
    """Exception raise if user try register object of incorrect type."""

    __slots__ = ()

    _text = 'Incorrect type of register object.'
    _code = 201


class FunctionRegisterTypeError(RegisterTypeError):
    """Exception raise if user try register some thing
    but function or coroutine."""

    __slots__ = ()

    _text = (
        'Incorrect type of register object. '
        'Function overloader can registering only functions or coroutines.'
    )
    _code = 202


class MissedAnnotations(RegisterTypeError):
    """Exception raise if register object hasn't annotations."""

    __slots__ = ()

    _text = 'For registering object it must has annotations.'
    _code = 203


class AnnotationCountError(RegisterTypeError):
    """Exception raise if overloader is strict and register object has more
    arguments with annotation than default object."""

    __slots__ = ()

    _text = 'Register object has more args with annotation than default.'
    _code = 204
