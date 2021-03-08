try:
    from functools import cached_property
except ImportError:
    from overload.utils.property import cached_property

from typing import (
    NamedTupleMeta,
    Dict,
    Any,
    Union,
    Optional,
    _GenericAlias,
    T,
    VT,
    KT,
    T_co,
    V_co,
    VT_co,
    T_contra,
    TypeVar,
    Tuple,
)
from collections.abc import (
    ByteString,
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

    def __repr__(self):
        return (f"<class 'OverloadType'> type={self.type} "
                f'v_types={self.v_types} k_types={self.k_types} '
                f'can_mixed_v={self.can_mixed_v}')

    def __str__(self):
        return f"_Type({self.type})"

    def __init__(
            self, type_: Union[type, TypeVar],
            v_types: Optional[Union['_Type', Tuple['_Type', ...]]] = None,
            k_types: Optional[Union['_Type', Tuple['_Type', ...]]] = None,
            can_mixed_v: bool = True,
    ):
        self.type = type_
        self.v_types = v_types
        self.k_types = k_types
        self._can_mixed_v = can_mixed_v

    def __eq__(self, other: '_Type') -> bool:
        if not isinstance(other, _Type):
            # Do not support not _Type class instance
            raise NotImplemented

        same_type = self.type == other.type

        if other.v_types:
            same_v_types = self.v_types == other.v_types
        else:
            same_v_types = True

        if other.k_types:
            same_k_types = self.k_types == other.k_types
        else:
            same_k_types = True

        same_m_v = self.can_mixed_v == other.can_mixed_v

        return same_type and same_v_types and same_k_types and same_m_v

    @property
    def type(self) -> type or TypeVar:
        """Stored type, can be instance of type or typing.TypeVar class."""
        return self._type

    @type.setter
    def type(self, type_: int) -> None:
        """Setter must use only for mapping."""
        self._type = type_

    @property
    def v_types(self) -> Union['_Type', Tuple['_Type', ...]]:
        """Expected types of variables, who contains into instance of
        stored type.
        Only for instance of typing.TypeVar class, who can take parameters.

        Example:
            for typing.TypeVar instance typing.List[str], v_types is 'str'.

        """
        return self._v_types

    @v_types.setter
    def v_types(self, types: Union['_Type', Tuple['_Type', ...]]) -> None:
        """Setter must use only for mapping."""
        self._v_types = types

    @property
    def k_types(self) -> Union['_Type', Tuple['_Type', ...]]:
        """Expected types of keys, who contains into instance of stored type.
        Only for instance of typing.TypeVar class,
        who can take key, value parameters.

        Example:
            for typing.TypeVar instance typing.Dict[int, str],
            k_types is 'int'.

        """
        return self._k_types

    @k_types.setter
    def k_types(self, types: Union['_Type', Tuple['_Type', ...]]) -> None:
        """Setter must use only for mapping."""
        self._k_types = types

    @property
    def can_mixed_v(self) -> bool:
        """Flag, about can mixed value types or must be an strict sequence."""
        return self._can_mixed_v


class _TypeHandler:
    """Class encapsulate method for work with types."""
    _IGNORED_OBJECTS = (
        Callable,
        Coroutine,
        Iterator,
        AsyncIterator,
        Generator,
        AsyncGenerator,
        AbstractContextManager,
        AbstractAsyncContextManager,
    )
    _TO_ANY_CONVERT = {
        T: Any,
        VT: Any,
        KT: Any,
        T_co: Any,
        V_co: Any,
        VT_co: Any,
        T_contra: Any,
        Union: Any,
        Optional: Any,
    }

    __slots__ = ('__dict__', '_deep')

    def __repr__(self) -> str:
        return "<class 'TypeHandler'>"

    def __str__(self) -> str:
        return 'Handler for python3 base types and types from typing module.'

    def __init__(self, deep=False):
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
        self._deep = deep

    def out_up_types(self, type_: Any) -> dict or Tuple[dict, ...]:
        """Convert type to _Type instance or tuple with _Type instances."""
        types, real_type, v_types, k_types, m_v = None, None, None, None, True

        try:
            real_type = type_.__origin__
            # handling Union and Optional types
            if real_type is Union or real_type is Optional:
                types = tuple(
                    self.out_up_types(type_) for type_ in type_.__args__
                )
            elif self._deep:
                # # handling function types
                if real_type not in self._IGNORED_OBJECTS:
                    try:
                        # Only typing.Tuple can contain fixed count of types
                        if real_type is tuple and len(type_.__args__) > 1:
                            if type_.__args__[-1] is Ellipsis:
                                v_types = self.out_up_types(type_.__args__[0])
                            else:
                                v_types = tuple(
                                    self.out_up_types(inner_type)
                                    for inner_type in type_.__args__
                                )
                                m_v = False
                        else:
                            v_types = self.out_up_types(type_.__args__[-1])

                            # object type is variation of dict
                            if len(type_.__args__) > 1:
                                k_types = self.out_up_types(type_.__args__[0])
                    except IndexError:
                        pass
        except AttributeError:
            real_type = self._TO_ANY_CONVERT.get(type_) or type_

        return types or _Type(real_type, v_types, k_types, m_v)

    def converting_annotations(
            self,
            annotations: Dict[str, type],
    ) -> Dict[str, _Type]:
        """Converting annotations types to overloader types."""
        for parameter, type_ in annotations.items():
            annotations[parameter] = self.out_up_types(type_)

        return annotations
