import typing
import collections
import contextlib
from types import FunctionType

from overload.type.type import _Type


class _UnknownType1:
    pass


class _UnknownType2:
    pass


OUT_UP_TYPES_AND_EXPECTATIONS = (
    # format: deep, input_type, expected
    # Native types
    # 0
    (True, None, _Type(None)),
    (True, type(None), _Type(type(None))),
    # 1
    (True, bytes, _Type(bytes)),
    (True, collections.abc.ByteString, _Type(collections.abc.ByteString)),
    # 2
    (True, bytearray, _Type(bytearray)),
    # 3
    (True, str, _Type(str)),
    (True, typing.Text, _Type(str)),
    # 4
    (True, int, _Type(int)),
    # 5
    (True, tuple, _Type(tuple)),
    (True, typing.Tuple, _Type(tuple)),
    (True, typing.Tuple[int], _Type(tuple)),
    (True, typing.Tuple[int, float, str], _Type(tuple)),
    (True, typing.Tuple[typing.Union[str, int]], _Type(tuple)),
    (True, typing.Tuple[typing.Union[str, int], ...], _Type(tuple)),
    # 6
    (True, dict, _Type(dict)),
    (True, typing.Dict, _Type(dict)),
    (True, typing.Dict[str, int], _Type(dict)),
    # 7
    (True, list, _Type(list)),
    (True, typing.List, _Type(list)),
    (True, typing.List[int], _Type(list)),
    # 8
    (True, set, _Type(set)),
    (True, typing.Set, _Type(set)),
    (True, typing.Set[int], _Type(set)),
    (False, typing.Set[int], _Type(set)),
    # 9
    (True, frozenset, _Type(frozenset)),
    (True, typing.FrozenSet, _Type(frozenset)),
    (True, typing.FrozenSet[int], _Type(frozenset)),
    # Collections types
    # 21
    (True, collections.ChainMap, _Type(collections.ChainMap)),
    (True, typing.ChainMap, _Type(collections.ChainMap)),
    (True, typing.ChainMap[str, int], _Type(collections.ChainMap)),
    # 22
    (True, collections.Counter, _Type(collections.Counter)),
    (True, typing.Counter, _Type(collections.Counter)),
    (True, typing.Counter[int], _Type(collections.Counter)),
    # 23
    (True, collections.deque, _Type(collections.deque)),
    (True, typing.Deque, _Type(collections.deque)),
    (True, typing.Deque[int], _Type(collections.deque)),
    # 24
    (True, collections.defaultdict, _Type(collections.defaultdict)),
    (True, typing.DefaultDict, _Type(collections.defaultdict)),
    (True, typing.DefaultDict[str, int], _Type(collections.defaultdict)),
    # 25
    (True, collections.OrderedDict, _Type(collections.OrderedDict)),
    (True, typing.OrderedDict, _Type(collections.OrderedDict)),
    (True, typing.OrderedDict[str, int], _Type(collections.OrderedDict)),
    # Other objects types
    # 31
    (True, collections.abc.Callable, _Type(FunctionType)),
    (True, typing.Callable, _Type(FunctionType)),
    (True, typing.Callable[[str, int], int], _Type(FunctionType)),
    # 32
    (True, collections.abc.Coroutine, _Type(FunctionType)),
    (True, typing.Coroutine, _Type(FunctionType)),
    (True, typing.Coroutine[str, int, int], _Type(FunctionType)),
    # 33
    (True, collections.abc.Iterator, _Type(FunctionType)),
    (True, typing.Iterator, _Type(FunctionType)),
    (True, typing.Iterator[str], _Type(FunctionType)),
    # 34
    (True, collections.abc.AsyncIterator, _Type(FunctionType)),
    (True, typing.AsyncIterator, _Type(FunctionType)),
    (True, typing.AsyncIterator[str], _Type(FunctionType)),
    # 35
    (True, collections.abc.Generator, _Type(FunctionType)),
    (True, typing.Generator, _Type(FunctionType)),
    (True, typing.Generator[str, int, int], _Type(FunctionType)),
    # 36
    (True, collections.abc.AsyncGenerator, _Type(FunctionType)),
    (True, typing.AsyncGenerator, _Type(FunctionType)),
    (True, typing.AsyncGenerator[str, int], _Type(FunctionType)),
    # 37
    (True, contextlib.AbstractContextManager, _Type(FunctionType)),
    (True, typing.ContextManager, _Type(FunctionType)),
    (True, typing.ContextManager[int], _Type(FunctionType)),
    # 38
    (True, contextlib.AbstractAsyncContextManager, _Type(FunctionType)),
    (True, typing.AsyncContextManager, _Type(FunctionType)),
    (True, typing.AsyncContextManager[int], _Type(FunctionType)),
    # Special types
    # Any
    (True, typing.Any, _Type(...)),
    # Optional
    (True, typing.Optional, _Type(...)),
    (True, typing.Optional[str], (_Type(str), _Type(type(None)))),
    # Union
    (True, typing.Union, (_Type(...))),
    (True, typing.Union[str, int], (_Type(str), _Type(int))),
    # Deep mixed type
    (True, typing.List[
        typing.Union[str, typing.Tuple[
            typing.Dict[int, typing.Optional[
                typing.Callable
            ]]
        ]]
    ],
     _Type(list)),
    # Unknown type
    (True, _UnknownType1, _Type(_UnknownType1)),
    # Not deep mixed type
    (False, typing.List[
        typing.Union[str, typing.Tuple[
            typing.Dict[int, typing.Optional[
                typing.Callable
            ]]
        ]]
    ],
     _Type(list)
     ),
)

CONVERTING_ARGS = (
    # Format: args, result.
    ((123, '123', [1, 2, 3]), (_Type(int), _Type(str), _Type(list))),
)
CONVERTING_KWARGS = (
    # Format: args, result.
    (
        {'int': 123, 'str': '123', 'list': [1, 2, 3]},
        {'int': _Type(int), 'str': _Type(str), 'list': _Type(list)}
    ),
)
