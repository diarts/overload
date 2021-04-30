from types import FunctionType
from typing import Callable, cast, Union
from overload.overloader.function import FunctionOverloader

__all__ = (
    'overload',
)


def overload(
        strict: bool = True,
        overlapping: bool = False
) -> Union[Callable, FunctionOverloader]:
    """Replace function to FunctionOverloader object.

    Args:
        strict (bool): Activate validation of implementation annotations
            count compared overload object annotations.
        overlapping (bool): Activate registration of implementation with
            same annotations as the default overload object.

    """
    if not isinstance(strict, bool):
        cls = FunctionOverloader(cast(FunctionType, strict))
        return cls

    def wrapper(function) -> FunctionOverloader:
        cls = FunctionOverloader(function, strict, overlapping)
        return cls

    return wrapper
