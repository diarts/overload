import typing
import collections
import contextlib

from overload.type.type import _Type


class _UnknownType1:
    pass


class _UnknownType2:
    pass


out_up_types_types_and_expectations = [
    # format: input_type, expected
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
    (True, typing.Tuple[int], _Type(tuple, _Type(int))),
    (True, typing.Tuple[int, float, str], _Type(
        type_=tuple,
        v_types=(
            _Type(int),
            _Type(float),
            _Type(str),
        ),
        can_mixed_v=False,
    )),
    # 6
    (True, dict, _Type(dict)),
    (True, typing.Dict, _Type(dict, _Type(typing.Any), _Type(typing.Any))),
    (True, typing.Dict[str, int], _Type(dict, _Type(int), _Type(str))),
    # 7
    (True, list, _Type(list)),
    (True, typing.List, _Type(list, _Type(typing.Any))),
    (True, typing.List[int], _Type(list, _Type(int))),
    # 8
    (True, set, _Type(set)),
    (True, typing.Set, _Type(set, _Type(typing.Any))),
    (True, typing.Set[int], _Type(set, _Type(int))),
    (False, typing.Set[int], _Type(set)),
    # 9
    (True, frozenset, _Type(frozenset)),
    (True, typing.FrozenSet, _Type(frozenset, _Type(typing.Any))),
    (True, typing.FrozenSet[int], _Type(frozenset, _Type(int))),
    # Collections types
    # 21
    (True, collections.ChainMap, _Type(collections.ChainMap)),
    (True, typing.ChainMap, _Type(collections.ChainMap, _Type(typing.Any),
                                  _Type(typing.Any))),
    (True, typing.ChainMap[str, int], _Type(collections.ChainMap, _Type(int),
                                            _Type(str))),
    # 22
    (True, collections.Counter, _Type(collections.Counter)),
    (True, typing.Counter, _Type(collections.Counter, _Type(typing.Any))),
    (True, typing.Counter[int], _Type(collections.Counter, _Type(int))),
    # 23
    (True, collections.deque, _Type(collections.deque)),
    (True, typing.Deque, _Type(collections.deque, _Type(typing.Any))),
    (True, typing.Deque[int], _Type(collections.deque, _Type(int))),
    # 24
    (True, collections.defaultdict, _Type(collections.defaultdict)),
    (True, typing.DefaultDict, _Type(collections.defaultdict,
                                     _Type(typing.Any),
                                     _Type(typing.Any))),
    (True, typing.DefaultDict[str, int], _Type(collections.defaultdict,
                                               _Type(int),
                                               _Type(str))),
    # 25
    (True, collections.OrderedDict, _Type(collections.OrderedDict)),
    (True, typing.OrderedDict, _Type(collections.OrderedDict,
                                     _Type(typing.Any),
                                     _Type(typing.Any))),
    (True, typing.OrderedDict[str, int], _Type(collections.OrderedDict,
                                               _Type(int),
                                               _Type(str))),
    # Other objects types
    # 31
    (True, collections.abc.Callable, _Type(collections.abc.Callable)),
    (True, typing.Callable, _Type(collections.abc.Callable)),
    (True, typing.Callable[[str, int], int], _Type(collections.abc.Callable)),
    # 32
    (True, collections.abc.Coroutine, _Type(collections.abc.Coroutine)),
    (True, typing.Coroutine, _Type(collections.abc.Coroutine)),
    (True, typing.Coroutine[str, int, int], _Type(collections.abc.Coroutine)),
    # 33
    (True, collections.abc.Iterator, _Type(collections.abc.Iterator)),
    (True, typing.Iterator, _Type(collections.abc.Iterator)),
    (True, typing.Iterator[str], _Type(collections.abc.Iterator)),
    # 34
    (True, collections.abc.AsyncIterator,
     _Type(collections.abc.AsyncIterator)),
    (True, typing.AsyncIterator, _Type(collections.abc.AsyncIterator)),
    (True, typing.AsyncIterator[str], _Type(collections.abc.AsyncIterator)),
    # 35
    (True, collections.abc.Generator, _Type(collections.abc.Generator)),
    (True, typing.Generator, _Type(collections.abc.Generator)),
    (True, typing.Generator[str, int, int], _Type(collections.abc.Generator)),
    # 36
    (True, collections.abc.AsyncGenerator,
     _Type(collections.abc.AsyncGenerator)),
    (True, typing.AsyncGenerator, _Type(collections.abc.AsyncGenerator)),
    (True, typing.AsyncGenerator[str, int],
     _Type(collections.abc.AsyncGenerator)),
    # 37
    (True, contextlib.AbstractContextManager, _Type(
        contextlib.AbstractContextManager)),
    (True, typing.ContextManager, _Type(contextlib.AbstractContextManager)),
    (True, typing.ContextManager[int],
     _Type(contextlib.AbstractContextManager)),
    # 38
    (True, contextlib.AbstractAsyncContextManager,
     _Type(contextlib.AbstractAsyncContextManager)),
    (True, typing.AsyncContextManager,
     _Type(contextlib.AbstractAsyncContextManager)),
    (True, typing.AsyncContextManager[int],
     _Type(contextlib.AbstractAsyncContextManager)),
    # Special types
    # Any
    (True, typing.Any, _Type(typing.Any)),
    # Optional
    (True, typing.Optional, _Type(typing.Any)),
    (True, typing.Optional[str], (_Type(str), _Type(type(None)))),
    # Union
    (True, typing.Union, (_Type(typing.Any))),
    (True, typing.Union[str, int], (_Type(str), _Type(int))),
    # Deep mixed type
    (True, typing.List[
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
]
