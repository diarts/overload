try:
    from functools import cached_property
except ImportError:
    from overload.utils.property import cached_property

from typing import (
    NamedTupleMeta,
    AnyStr,
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
from collections import (
    ChainMap,
    Counter,
    deque,
    defaultdict,
    OrderedDict,
)
from contextlib import AbstractContextManager, AbstractAsyncContextManager


class _Type:
    """Class contained overloading type and it parameters
    for typing.TypeVar instance."""
    __slots__ = ('_type', '_v_types', '_k_types', '_can_mixed_v')

    def __repr__(self):
        return (f'<class Overload Type> type={self.type} '
                f'v_types={self.v_types} k_types={self.k_types}')

    def __init__(
            self, type_: Union[type, TypeVar],
            v_types: Optional[Union['_Type', Tuple['_Type', ...]]] = None,
            k_types: Optional[Union['_Type', Tuple['_Type', ...]]] = None,
            can_mixed_v: bool = True,
    ):
        self._type = type_
        self._v_types = v_types
        self._k_types = k_types
        self._can_mixed_v = can_mixed_v

    def __eq__(self, other: '_Type') -> bool:
        if not isinstance(other, _Type):
            # not support not _Type class instance
            raise NotImplemented

        same_type = self.type == other.type
        same_v_types = self.v_types == other.v_types
        same_k_types = self.v_types == other.v_types
        same_m_v = self.can_mixed_v == other.can_mixed_v

        return same_type and same_v_types and same_k_types and same_m_v

    @property
    def type(self):
        """Stored type, can be instance of type or typing.TypeVar class."""
        return self._type

    @property
    def v_types(self):
        """Expected types of variables, who contains into instance of
        stored type.
        Only for instance of typing.TypeVar class, who can take parameters.

        Example:
            for typing.TypeVar instance typing.List[str]
            v_types is 'str'.

        """
        return self._v_types

    @property
    def k_types(self):
        """Expected types of keys, who contains into instance of stored type.
        Only for instance of typing.TypeVar class,
        who can take key, value parameters.

        Example:
            for typing.TypeVar instance typing.Dict[int, str]
            k_types is 'int'.

        """
        return self._k_types

    @property
    def can_mixed_v(self):
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

    __slots__ = ('__dict__',)

    def __repr__(self):
        return '<class Type Handler>'

    def __str__(self):
        return 'Handler for python3 base types and types from typing module.'

    @cached_property
    def mapper(self) -> ChainMap:
        """Mapping type to id."""
        native = {
            type(None): 0,
            None: 0,
            bytes: 1,
            ByteString: 1,
            bytearray: 2,
            str: 3,
            int: 4,
            tuple: 5,
            dict: 6,
            list: 7,
            set: 8,
            frozenset: 9,
        }
        collections = {
            ChainMap: 21,
            Counter: 22,
            deque: 23,
            defaultdict: 24,
            OrderedDict: 25,
        }
        objects = {
            Callable: 31,
            Coroutine: 32,
            Iterator: 33,
            AsyncIterator: 34,
            Generator: 35,
            AsyncGenerator: 36,
            AbstractContextManager: 37,
            AbstractAsyncContextManager: 38,
        }
        any_str = frozenset({
            native[str],
            native[bytes],
            native[ByteString],
        })

        any_ = set(native.values())
        any_ |= set(collections.values())
        any_ |= set(objects.values())
        any_ |= any_str
        any_ = frozenset(any_)

        multiplicity = {
            AnyStr: any_str,
            Any: any_,
        }
        return ChainMap(native, collections, objects, multiplicity)

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
            else:
                # # handling function types
                if real_type not in self._IGNORED_OBJECTS:
                    try:
                        # Only typing.Tuple can contain fixed count of types
                        if real_type is tuple and len(type_.__args__) > 1:
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
            if type_ is Union or type_ is Optional:
                real_type = Any
            else:
                real_type = type_

        return types or _Type(real_type, v_types, k_types, m_v)
