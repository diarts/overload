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

from overload.exception.type import *


class _Type:
    """Class contained overloading type and it parameters
    for typing.TypeVar instance."""
    __slots__ = ('_type', '_v_types', '_k_types', '_can_mixed_v')

    def __repr__(self):
        return (f'<class Overload Type> type={self.type} '
                f'v_types={self.v_types} k_types={self.k_types} '
                f'can_mixed_v={self.can_mixed_v}')

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
            # not support not _Type class instance
            raise NotImplemented

        same_type = self.type == other.type
        same_v_types = self.v_types == other.v_types
        same_k_types = self.v_types == other.v_types
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
            for typing.TypeVar instance typing.List[str]
            v_types is 'str'.

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
            for typing.TypeVar instance typing.Dict[int, str]
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

    __custom_types__ = None
    _last_custom_types_id = 99

    __slots__ = ('__dict__',)

    def __repr__(self) -> str:
        return '<class Type Handler>'

    def __str__(self) -> str:
        return 'Handler for python3 base types and types from typing module.'

    def __init__(self):
        self.__custom_types__ = {}

    def __getitem__(self, type_) -> int:
        """Convert python3 type to overload module type id."""
        try:
            return self.mapper[type_]
        except KeyError:
            try:
                return self.__custom_types__[type_]
            except KeyError:
                raise UnknownType(type_)

    def __setitem__(self, type_: type, index: int = None) -> int:
        """Add new type item into __custom_types__ dict."""
        if type(type_) is not type:
            raise CustomTypeError(type_)

        # check new type to exist it current mapper
        try:
            self[type_]
        except UnknownType:
            pass
        else:
            raise CustomTypeAlreadyExist(type_, self[type_])

        # validate new index
        if index and (
                type(index) is not int
                or index in range(0, 100)
                or index in self.__custom_types__.values()):
            raise IndexValueError()

        # update last index
        if index and index > self._last_custom_types_id:
            self._last_custom_types_id = index
        else:
            self._last_custom_types_id += 1

        self.__custom_types__[type_] = self._last_custom_types_id

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
            real_type = type_

        return types or _Type(real_type, v_types, k_types, m_v)

    def _mapping_type(self, type_: _Type, add_unknown=False) -> _Type:
        """Convert _Type object to _Type with indexes of arg type, value types
        and key types.

        Example:
            inputs format:
                _Type(
                    type_ = int,
                    v_types = (
                        _Type(str),
                        _Type(list, (str), None),
                    k_types = None
                )
            return format:
                _Type(
                    type_ = 3,
                    v_types = _Type(4), _Type(3, _Type(7)),
                    k_type = None
                )
        """
        # map type
        try:
            type_.type = self[type_.type]
        except UnknownType:
            if add_unknown:
                self[type_.type] = None
                type_.type = self._last_custom_types_id
            else:
                raise UnknownType(type_.type)

        # map v_types
        if type_.v_types:
            try:
                type_.v_types = tuple(
                    self._mapping_type(v) for v in type_.v_types
                )
            except TypeError:
                type_.v_types = self._mapping_type(type_.v_types)

        # map k_types
        if type_.k_types:
            try:
                type_.k_types = tuple(
                    self._mapping_type(k) for k in type_.k_types
                )
            except TypeError:
                type_.k_types = self._mapping_type(type_.k_types)

        return type_
