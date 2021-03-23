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

__all__ = ()


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

    @cached_property
    def _hash(self) -> str:
        """Generate unique string hash."""
        hash_ = list(str(hash(self.type)))

        return ''.join(hash_)

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

        return self.type == other.type

    def __hash__(self) -> int:
        return hash(self._hash)


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
        types, real_type, v_types, k_types = None, None, None, None
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

        # Handling Union and Optional types.
        if real_type is Union or real_type is Optional:
            if getattr(type_, '__args__', None):
                types = tuple(
                    self.out_up_types(type_) for type_ in type_.__args__
                )
            else:
                real_type = Ellipsis

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

        return types or _Type(real_type)

    def converting_annotations(
            self,
            annotations: Dict[str, type],
    ) -> Dict[str, _Type]:
        """Converting annotations types to overloader types."""
        for parameter, type_ in annotations.items():
            annotations[parameter] = cast(type, self.out_up_types(type_))

        # Fake type converting.
        annotations = cast(Dict[str, _Type], annotations)

        return annotations

    def extract_type(self, value: Any) -> _Type:
        """Convert value to instance of _Type."""
        return self.out_up_types(type(value))

    def converting_args(self, args: Tuple[Any, ...]) -> Tuple[_Type, ...]:
        """Converting all call args values to _Type instances."""
        return tuple(map(self.extract_type, args))

    def converting_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, _Type]:
        """Converting all call kwargs values to _Type instances."""
        return {key: self.extract_type(value) for key, value in kwargs.items()}
