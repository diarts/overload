try:
    from functools import cached_property
except ImportError:
    from overload.utils.property import cached_property

from types import FunctionType
from typing import (
    Dict,
    Any,
    Union,
    Optional,
    T,
    VT,
    KT,
    T_co,
    V_co,
    VT_co,
    T_contra,
    TypeVar,
    Tuple,
    # Functions.
    cast,
    # Other.
    Generic
)
from collections.abc import (
    Callable,
    Coroutine,
    Iterator,
    AsyncIterator,
    Generator,
    AsyncGenerator,
)
from contextlib import AbstractContextManager, AbstractAsyncContextManager

__all__ = (
    'Args',
    'Kwargs'
)


class _Type:
    """Class contained overloading type and it parameters
    for typing.TypeVar instance."""
    __slots__ = ('_type', '_v_types', '_k_types', '_can_mixed_v')

    def __init__(
            self, type_: Union[type, TypeVar],
    ):
        self._type = type_
        self._v_types = None
        self._k_types = None
        self._can_mixed_v = True

    @property
    def type(self) -> type or TypeVar:
        """Stored type, can be instance of type or typing.TypeVar class."""
        return self._type

    @property
    def v_types(self) -> Tuple['_Type', ...]:
        """Expected types of variables, who contains into instance of
        stored type.
        Only for instance of typing.TypeVar class, who can take parameters.

        Example:
            for typing.TypeVar instance typing.List[str], v_types is 'str'.

        """
        return self._v_types

    @property
    def k_types(self) -> Tuple['_Type', ...]:
        """Expected types of keys, who contains into instance of stored type.
        Only for instance of typing.TypeVar class,
        who can take key, value parameters.

        Example:
            for typing.TypeVar instance typing.Dict[int, str],
            k_types is 'int'.

        """
        return self._k_types

    @property
    def can_mixed_v(self) -> bool:
        """Flag, about can mixed value types or must be an strict sequence."""
        return self._can_mixed_v

    def __repr__(self):
        return (f"<class 'OverloadType'> type={self.type} "
                f'v_types={self.v_types} k_types={self.k_types} '
                f'can_mixed_v={self.can_mixed_v}')

    def __str__(self):
        return f"_Type({self.type})"

    def __eq__(self, other: '_Type') -> bool:
        if not isinstance(other, _Type):
            # Do not support not _Type class instance
            raise ValueError('_Type object can be compared only with self.')

        if self.type is Ellipsis or other.type is Ellipsis:
            return True

        return self.type == other.type

    def __hash__(self):
        return hash(self.type)


class _SingleType:
    """Base type for single types."""
    __slots__ = ('_types',)

    _types: Tuple[Any, ...]

    def __init__(self, types: Tuple[_Type, ...]):
        self._types = types

    @property
    def types(self):
        """Tuple of contain types."""
        return self._types

    def __repr__(self) -> str:
        return f'< {self.__str__()} with types={self.types}>'

    def __str__(self) -> str:
        return self.__class__.__name__

    def __contains__(self, item):
        return item in self.types

    def __eq__(self, other):
        if not isinstance(other, _SingleType):
            return False
        else:
            return self.types == other.types


class _ArgsType(_SingleType):
    pass


class _KwargsType(_SingleType):
    pass


class _TypeHandler:
    """Class encapsulate method for work with types."""
    _FUNCTION_INTERPRET = (
        Callable,
        Coroutine,
        Iterator,
        AsyncIterator,
        Generator,
        AsyncGenerator,
        AbstractContextManager,
        AbstractAsyncContextManager,
    )
    _ELLIPSIS_CONVERT = (
        T,
        VT,
        KT,
        T_co,
        V_co,
        VT_co,
        T_contra,
        Any,
    )

    __slots__ = ('__dict__', '_deep')

    def __repr__(self) -> str:
        return "<class 'TypeHandler'>"

    def __str__(self) -> str:
        return 'Handler for python3 base types and types from typing module.'

    def __init__(self):
        """
        Args:
            deep (Bool, optional): Check inner field types of arguments (True)
                or only arguments types (False).
                Default value = False.

                example deep=True:
                    List[str] -> _Type(
                            type=list,
                            v_type=(_Type(str)
                        ))
                example deep=False:
                    List[str] -> _Type(list)

        """
        # Start realisation without deep functional.
        self._deep = False

    def out_up_types(self, type_: Any, ) -> Union[_Type, Tuple[_Type, ...]]:
        """Convert type to _Type instance or tuple with _Type instances."""
        real_type, v_types, k_types = None, None, None
        type_class = _Type
        can_mixed: bool = True

        try:
            real_type = type_.__origin__
        except AttributeError:
            if type_ in self._ELLIPSIS_CONVERT:
                real_type = Ellipsis
            else:
                real_type = type_
        finally:
            if real_type in self._FUNCTION_INTERPRET:
                real_type = FunctionType
            elif real_type is Args:
                type_class = _ArgsType
            elif real_type is Kwargs:
                type_class = _KwargsType

        # Handling Union and Optional types.
        if real_type in (Args, Kwargs, Union, Optional):
            try:
                type_args = type_.__args__
            except AttributeError:
                type_args = (Any,)

            real_type = []

            for in_type in type_args:
                new_type = self.out_up_types(in_type)

                if isinstance(new_type, tuple):
                    real_type.extend(new_type)
                else:
                    real_type.append(new_type)

            real_type = tuple(real_type)
        # Handling inner types.
        # elif self._deep:
        #     try:
        #         # Only typing.Tuple can contain fixed count of types.
        #         if real_type is tuple:
        #             if type_.__args__[-1] is not Ellipsis:
        #                 can_mixed = False
        #
        #             v_types = tuple(
        #                 self.out_up_types(inner)
        #                 for inner in type_.__args__[:(-1 - can_mixed)]
        #             )
        #
        #         # Not tuple.
        #         else:
        #             v_types = tuple(
        #                 self.out_up_types(type_.__args__[-1])
        #             )
        #
        #         # object type is variation of dict
        #         if len(type_.__args__) > 1:
        #             k_types = tuple(
        #                 self.out_up_types(type_.__args__[0])
        #             )
        #     except IndexError:
        #         pass

        # Generate output result.
        real_type_is_tuple = isinstance(real_type, tuple)
        is_single_subclass = issubclass(type_class, _SingleType)
        if real_type_is_tuple and not is_single_subclass:
            type_ = real_type
        else:
            type_ = type_class(real_type)

        return type_

    def converting_annotations(
            self,
            annotations: Dict[str, type],
    ) -> Dict[str, _Type]:
        """Converting annotations types to overloader types."""
        new_annotations = {}

        for parameter, type_ in annotations.items():
            new_annotations[parameter] = cast(type, self.out_up_types(type_))

        # Fake type converting.
        new_annotations = cast(Dict[str, _Type], new_annotations)

        return new_annotations

    def extract_type(self, value: Any) -> _Type:
        """Convert value to instance of _Type."""
        return self.out_up_types(type(value))

    def converting_args(self, args: Tuple[Any, ...]) -> Tuple[_Type, ...]:
        """Converting all call args values to _Type instances."""
        return tuple(map(self.extract_type, args))

    def converting_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, _Type]:
        """Converting all call kwargs values to _Type instances."""
        return {key: self.extract_type(value) for key, value in kwargs.items()}


class Args(Generic[T]):
    pass


class Kwargs(Generic[T]):
    pass
