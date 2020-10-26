import typing
import collections
import contextlib

from overload.type.type import _Type
from overload.exception.type import (
    CustomTypeError,
    CustomTypeAlreadyExist,
    IndexValueError,
)


class _UnknownType1:
    pass


class _UnknownType2:
    pass


out_up_types_types_and_expectations = [
    # Native types
    # 0
    (None, _Type(None)),
    (type(None), _Type(type(None))),
    # 1
    (bytes, _Type(bytes)),
    (collections.abc.ByteString, _Type(collections.abc.ByteString)),
    # 2
    (bytearray, _Type(bytearray)),
    # 3
    (str, _Type(str)),
    (typing.Text, _Type(str)),
    # 4
    (int, _Type(int)),
    # 5
    (tuple, _Type(tuple)),
    (typing.Tuple, _Type(tuple)),
    (typing.Tuple[int], _Type(tuple, _Type(int))),
    (typing.Tuple[int, float, str], _Type(
        type_=tuple,
        v_types=(
            _Type(int),
            _Type(float),
            _Type(str),
        ),
        can_mixed_v=False,
    )),
    # 6
    (dict, _Type(dict)),
    (typing.Dict, _Type(dict, _Type(typing.VT), _Type(typing.KT))),
    (typing.Dict[str, int], _Type(dict, _Type(int), _Type(str))),
    # 7
    (list, _Type(list)),
    (typing.List, _Type(list, _Type(typing.T))),
    (typing.List[int], _Type(list, _Type(int))),
    # 8
    (set, _Type(set)),
    (typing.Set, _Type(set, _Type(typing.T))),
    (typing.Set[int], _Type(set, _Type(int))),
    # 9
    (frozenset, _Type(frozenset)),
    (typing.FrozenSet, _Type(frozenset, _Type(typing.T_co))),
    (typing.FrozenSet[int], _Type(frozenset, _Type(int))),
    # Collections types
    # 21
    (collections.ChainMap, _Type(collections.ChainMap)),
    (typing.ChainMap, _Type(collections.ChainMap, _Type(typing.VT),
                            _Type(typing.KT))),
    (typing.ChainMap[str, int], _Type(collections.ChainMap, _Type(int),
                                      _Type(str))),
    # 22
    (collections.Counter, _Type(collections.Counter)),
    (typing.Counter, _Type(collections.Counter, _Type(typing.T))),
    (typing.Counter[int], _Type(collections.Counter, _Type(int))),
    # 23
    (collections.deque, _Type(collections.deque)),
    (typing.Deque, _Type(collections.deque, _Type(typing.T))),
    (typing.Deque[int], _Type(collections.deque, _Type(int))),
    # 24
    (collections.defaultdict, _Type(collections.defaultdict)),
    (typing.DefaultDict, _Type(collections.defaultdict, _Type(typing.VT),
                               _Type(typing.KT))),
    (typing.DefaultDict[str, int], _Type(collections.defaultdict, _Type(int),
                                         _Type(str))),
    # 25
    (collections.OrderedDict, _Type(collections.OrderedDict)),
    (typing.OrderedDict, _Type(collections.OrderedDict, _Type(typing.VT),
                               _Type(typing.KT))),
    (typing.OrderedDict[str, int], _Type(collections.OrderedDict, _Type(int),
                                         _Type(str))),
    # Other objects types
    # 31
    (collections.abc.Callable, _Type(collections.abc.Callable)),
    (typing.Callable, _Type(collections.abc.Callable)),
    (typing.Callable[[str, int], int], _Type(collections.abc.Callable)),
    # 32
    (collections.abc.Coroutine, _Type(collections.abc.Coroutine)),
    (typing.Coroutine, _Type(collections.abc.Coroutine)),
    (typing.Coroutine[str, int, int], _Type(collections.abc.Coroutine)),
    # 33
    (collections.abc.Iterator, _Type(collections.abc.Iterator)),
    (typing.Iterator, _Type(collections.abc.Iterator)),
    (typing.Iterator[str], _Type(collections.abc.Iterator)),
    # 34
    (collections.abc.AsyncIterator, _Type(collections.abc.AsyncIterator)),
    (typing.AsyncIterator, _Type(collections.abc.AsyncIterator)),
    (typing.AsyncIterator[str], _Type(collections.abc.AsyncIterator)),
    # 35
    (collections.abc.Generator, _Type(collections.abc.Generator)),
    (typing.Generator, _Type(collections.abc.Generator)),
    (typing.Generator[str, int, int], _Type(collections.abc.Generator)),
    # 36
    (collections.abc.AsyncGenerator, _Type(collections.abc.AsyncGenerator)),
    (typing.AsyncGenerator, _Type(collections.abc.AsyncGenerator)),
    (typing.AsyncGenerator[str, int], _Type(collections.abc.AsyncGenerator)),
    # 37
    (contextlib.AbstractContextManager, _Type(
        contextlib.AbstractContextManager)),
    (typing.ContextManager, _Type(contextlib.AbstractContextManager)),
    (typing.ContextManager[int], _Type(contextlib.AbstractContextManager)),
    # 38
    (contextlib.AbstractAsyncContextManager,
     _Type(contextlib.AbstractAsyncContextManager)),
    (typing.AsyncContextManager,
     _Type(contextlib.AbstractAsyncContextManager)),
    (typing.AsyncContextManager[int],
     _Type(contextlib.AbstractAsyncContextManager)),
    # Special types
    # Any
    (typing.Any, _Type(typing.Any)),
    # Optional
    (typing.Optional, _Type(typing.Optional)),
    (typing.Optional[str], (_Type(str), _Type(type(None)))),
    # Union
    (typing.Union, (_Type(typing.Union))),
    (typing.Union[str, int], (_Type(str), _Type(int))),
    # Deep mixed type
    (typing.List[
         typing.Union[str, typing.Tuple[
             typing.Dict[int, typing.Optional[
                 typing.Callable
             ]]
         ]]
     ],
     _Type(
         type_=list,
         v_types=(
             _Type(str),
             _Type(
                 type_=tuple,
                 v_types=_Type(
                     type_=dict,
                     k_types=_Type(int),
                     v_types=(
                         _Type(collections.abc.Callable),
                         _Type(type(None)),
                     )
                 )
             ),
         )
     )
     ),
    # Unknown type
    (_UnknownType1, _Type(_UnknownType1)),
]

set_custom_type_index = [
    # type errors
    (CustomTypeError, 5, None),
    (CustomTypeAlreadyExist, int, None),
    # correct add
    (None, _UnknownType1, 100),
    # index errors
    (IndexValueError, _UnknownType2, 99),
    (IndexValueError, _UnknownType2, 'test'),
    (IndexValueError, _UnknownType2, 100),
]
