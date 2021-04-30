from typing import Union

from overload.implementation.function import FunctionImplementation
from overload.type.type import _Type, Args, Kwargs, _TypeHandler

try:
    from functools import cached_property

    python_version_3_8 = True
except ImportError:
    python_version_3_8 = False

TypeHandler = _TypeHandler()


# ---------------------------- FUNCTION FOR TESTS -----------------------------
# Function without annotations.
def function_1():
    pass


implementation_1 = FunctionImplementation(
    function_1,
    TypeHandler.converting_annotations(function_1.__annotations__)
)


# Function with one args parameter with annotation.
def function_2(a: int):
    pass


implementation_2 = FunctionImplementation(
    function_2,
    TypeHandler.converting_annotations(function_2.__annotations__)
)


# Function with one only kwargs parameter with annotation.
def function_3(*, a: int):
    pass


implementation_3 = FunctionImplementation(
    function_3,
    TypeHandler.converting_annotations(function_3.__annotations__)
)


# Function with 2 args parameters, one with default.
def function_4(a: int, b: str = 'test'):
    pass


implementation_4 = FunctionImplementation(
    function_4,
    TypeHandler.converting_annotations(function_4.__annotations__)
)


# Function with infinite args contained any types.
def function_5(*args: Args):
    pass


implementation_5 = FunctionImplementation(
    function_5,
    TypeHandler.converting_annotations(function_5.__annotations__)
)


# Function with infinite args contained int.
def function_6(*args: Args[int]):
    pass


implementation_6 = FunctionImplementation(
    function_6,
    TypeHandler.converting_annotations(function_6.__annotations__)
)


# Function with infinite args without annotations.
def function_7(a: int, b: str = 'test', *args):
    pass


implementation_7 = FunctionImplementation(
    function_7,
    TypeHandler.converting_annotations(function_7.__annotations__)
)


# Function with 2 only kwargs parameters, one with default.
def function_8(*, a: int, b: str = 'test'):
    pass


implementation_8 = FunctionImplementation(
    function_8,
    TypeHandler.converting_annotations(function_8.__annotations__)
)


# Function with infinite kwargs contained any types.
def function_9(**kwargs: Kwargs):
    pass


implementation_9 = FunctionImplementation(
    function_9,
    TypeHandler.converting_annotations(function_9.__annotations__)
)


# Function with infinite kwargs contained int and str.
def function_10(**kwargs: Kwargs[Union[int, str]]):
    pass


implementation_10 = FunctionImplementation(
    function_10,
    TypeHandler.converting_annotations(function_10.__annotations__)
)


# Function with infinite kwargs without annotations.
def function_11(**kwargs):
    pass


implementation_11 = FunctionImplementation(
    function_11,
    TypeHandler.converting_annotations(function_11.__annotations__)
)


# Function with args and kwargs parameters with default.
def function_12(a: int, b: str = 'test', *, c: int, d: str = 'test'):
    pass


implementation_12 = FunctionImplementation(
    function_12,
    TypeHandler.converting_annotations(function_12.__annotations__)
)


# Function with all variance of parameter types.
def function_13(a: int, b: str = 'test', *args: Args[int],
                c: int, d: str = 'test', **kwargs: Kwargs[int]):
    pass


implementation_13 = FunctionImplementation(
    function_13,
    TypeHandler.converting_annotations(function_13.__annotations__)
)

TEST_FUNCTION_IMPLEMENTATION_COMPARE = (
    # Parameter format: implementation, named, unnamed, compare_result
    # Function 1 - without parameters.
    # Correct.
    # Empty args.
    (implementation_1, {}, (), True),  # 0
    # Wrong.
    # Set kwargs.
    (implementation_1, {'a': _Type(int)}, (), False),  # 1
    # Set args.
    (implementation_1, {}, (_Type(int),), False),  # 2
    # Set args and kwargs.
    (implementation_1, {'a': _Type(int)}, (_Type(int),), False),  # 3

    # Function 2 - 1 args parameter.
    # Correct.
    # Set args.
    (implementation_2, {}, (_Type(int),), True),  # 4
    # Set kwargs.
    (implementation_2, {'a': _Type(int)}, (), True),  # 5
    # Wrong.
    # Set args and kwargs.
    (implementation_2, {'a': _Type(int)}, (_Type(int),), False),  # 6
    # Set excess second parameter in args.
    (implementation_2, {}, (_Type(int), _Type(int),), False),  # 7
    # Set excess 'b' parameter in kwargs.
    (implementation_2, {'a': _Type(int), 'b': _Type(str)}, (), False),  # 8
    # Set wrong type value in args.
    (implementation_2, {}, (_Type(str),), False),  # 9
    # Set wrong type value in kwargs.
    (implementation_2, {'a': _Type(str)}, (), False),  # 10
    # Set correct parameter in kwargs and excess parameter in args.
    (implementation_2, {'a': _Type(int)}, (_Type(str),), False),  # 11
    # Set correct parameter in args and excess parameter 'b' in kwargs.
    (implementation_2, {'b': _Type(str)}, (_Type(int),), False),  # 12

    # Function 3 - 1 only kwargs parameter.
    # Correct.
    # Set kwargs.
    (implementation_3, {'a': _Type(int)}, (), True),  # 13
    # Wrong.
    # Set args.
    (implementation_3, {}, (_Type(int),), False),  # 14
    # Set args and kwargs.
    (implementation_3, {'a': _Type(int)}, (_Type(int),), False),  # 15
    # Set excess parameter in args.
    (implementation_3, {'a': _Type(int)}, (_Type(str),), False),  # 16
    # Set excess 'b' parameter in kwargs.
    (implementation_3, {'a': _Type(int), 'b': _Type(str)}, (), False),  # 17
    # Set wrong type value in kwargs.
    (implementation_3, {'a': _Type(str)}, (), False),  # 18

    # Function 4 - 2 args, one with default.
    # Correct.
    # Set args.
    (implementation_4, {}, (_Type(int), _Type(str)), True),  # 19
    # Set args, without parameter with default.
    (implementation_4, {}, (_Type(int),), True),  # 20
    # Set kwargs.
    (implementation_4, {'a': _Type(int), 'b': _Type(str)}, (), True),  # 21
    # Set kwargs, mixed.
    (implementation_4, {'b': _Type(str), 'a': _Type(int)}, (), True),  # 22
    # Set kwargs, without parameter with default.
    (implementation_4, {'a': _Type(int)}, (), True),  # 23
    # Set args and kwargs.
    (implementation_4, {'b': _Type(str)}, (_Type(int),), True),  # 25
    # Wrong.
    # Set args and kwargs, reverse.
    (implementation_4, {'a': _Type(int)}, (_Type(str),), False),  # 24
    # First parameter value args.
    (implementation_4, {}, (_Type(str), _Type(str)), False),  # 26
    # Second parameter value args.
    (implementation_4, {}, (_Type(int), _Type(int)), False),  # 27
    # First parameter value kwargs.
    (implementation_4, {'a': _Type(str), 'b': _Type(str)}, (), False),  # 28
    # Second parameter value kwargs.
    (implementation_4, {'a': _Type(int), 'b': _Type(int)}, (), False),  # 29
    # First parameter value kwargs, second correct in args.
    (implementation_4, {'a': _Type(str)}, (_Type(str)), False),  # 30
    # Second parameter value kwargs, first correct in args.
    (implementation_4, {'b': _Type(int)}, (_Type(int),), False),  # 31
    # Mixed parameter in args.
    (implementation_4, {}, (_Type(str), _Type(int),), False),  # 32
    # Missed parameter without default, second in args.
    (implementation_4, {}, (_Type(str),), False),  # 33
    # Missed parameter without default, second in kwargs.
    (implementation_4, {'b': _Type(str)}, (), False),  # 34
    # Set excess parameter in args.
    (
        implementation_4,
        {'a': _Type(int)},
        (_Type(str), _Type(int)),
        False,
    ),  # 35
    # Set excess 'c' parameter in kwargs.
    (implementation_4, {'a': _Type(int), 'c': _Type(str)}, (), False),  # 36

    # Function 5 - infinite args without types.
    # Correct.
    # Set many args with different parameters type.
    (implementation_5, {}, (_Type(int), _Type(str), _Type(list)), True),  # 37
    # Wrong.
    # Set args and kwargs parameters.
    (implementation_5, {'a': _Type(list)}, (_Type(int),), False),  # 38
    # Set many kwargs with different parameters.
    (implementation_5, {'a': _Type(list), 'b': _Type(int), }, (), False),  # 39

    # Function 6 - infinite args with type int.
    # Correct.
    # Set many args with single parameter type.
    (implementation_6, {}, (_Type(int), _Type(int), _Type(int)), True),  # 40
    # Wrong.
    # Set many args with different parameters type.
    (implementation_6, {}, (_Type(int), _Type(str), _Type(list)), False),  # 41
    # Set args and kwargs parameters.
    (implementation_6, {'a': _Type(int)}, (_Type(int),), False),  # 42
    # Set many kwargs with different parameters.
    (implementation_6, {'a': _Type(int), 'b': _Type(int), }, (), False),  # 43

    # Function 7 - not tracking infinite args and 2 args parameters,
    # 1 with default.
    # Wrong.
    # Many optional args, except registered 2 args parameters.
    (
        implementation_7,
        {},
        (_Type(int), _Type(str), _Type(int), _Type(list)),
        False,
    ),  # 44

    # Function 8 - 2 kwargs, one with default.
    # Correct.
    # Set kwarg parameter without defaults.
    (implementation_8, {'a': _Type(int)}, (), True),  # 45
    # Set all kwarg parameter.
    (implementation_8, {'a': _Type(int), 'b': _Type(str)}, (), True),  # 46
    # Wrong.
    # Set one of kwarg to arg.
    (implementation_8, {'a': _Type(int)}, (_Type(str),), False),  # 47
    # Set all parameters to args.
    (implementation_8, {}, (_Type(int), _Type(str),), False),  # 48
    # Wrong 'a' type.
    (implementation_8, {'a': _Type(str)}, (), False),  # 49
    # Wrong 'b' type.
    (implementation_8, {'a': _Type(int), 'b': _Type(int)}, (), False),  # 50
    # Missed 'a' parameter.
    (implementation_8, {'b': _Type(int)}, (), False),  # 51
    # Excess parameters in args.
    (implementation_8, {'a': _Type(int)}, (_Type(list),), False),  # 52
    # Excess parameters in kwargs.
    (implementation_8, {'a': _Type(int), 'e': _Type(list)}, (), False),  # 53

    # Function 9  - infinite kwargs without types.
    # Correct.
    (implementation_9, {'a': _Type(list), 'b': _Type(int)}, (), True),  # 54
    # Wrong.
    # Parameters in args and kwargs.
    (implementation_9, {'a': _Type(list)}, (_Type(int),), False),  # 55
    # Parameter in args.
    (implementation_9, {}, (_Type(list), _Type(int),), False),  # 56

    # Function 10 - infinite kwargs with types.
    # Correct.
    (
        implementation_10,
        {'a': _Type(int), 'b': _Type(str), 'c': _Type(int)},
        (),
        True,
    ),
    # Wrong.
    # Wrong parameter type.
    (implementation_10, {'a': _Type(list), 'b': _Type(str)}, (), False),

    # Function 11 - not registered infinite kwargs.
    # Correct
    (implementation_11, {}, (), True),
    # Wrong.
    # Set kwargs parameter.
    (implementation_11, {'a': _Type(int)}, (), False),
    # Set args parameter.
    (implementation_11, {}, (_Type(int),), False),
    # Set kwargs ans args parameters.
    (implementation_11, {'a': _Type(int)}, (_Type(int),), False),

    # Function 12 - 2 args and 2 kwargs parameters with 1 args with default
    # and 1 kwargs with default.
    # Correct.
    # Set all parameters.
    (
        implementation_12,
        {'c': _Type(int), 'd': _Type(str)},
        (_Type(int), _Type(str)),
        True,
    ),
    # Set parameter without defaults.
    (
        implementation_12,
        {'c': _Type(int)},
        (_Type(int),),
        True,
    ),
    # Set all parameters as kwargs.
    (
        implementation_12,
        {
            'a': _Type(int),
            'b': _Type(str),
            'c': _Type(int),
            'd': _Type(str),
        },
        (),
        True,
    ),
    # Set all parameters without default as kwargs.
    (
        implementation_12,
        {
            'a': _Type(int),
            'c': _Type(int),
        },
        (),
        True,
    ),
    # Wrong.
    # Set all parameters without default as kwargs and parameter 'b' as args.
    (
        implementation_12,
        {
            'a': _Type(int),
            'c': _Type(int),
        },
        (_Type(str),),
        False,
    ),
    # Set all as args.
    (
        implementation_12,
        {},
        (_Type(int), _Type(str), _Type(int), _Type(str)),
        False,
    ),

    # Function 13 - 2 args and 2 kwargs parameters with 1 args with default
    # and 1 kwargs with default and with infinite args and kwargs.
    # Correct.
    # Set all parameters and args and kwargs.
    (
        implementation_13,
        {
            "c": _Type(int),
            "d": _Type(str),
            "e": _Type(int),
        },
        (_Type(int), _Type(str), _Type(int), _Type(int)),
        True,
    ),
    # Set without default parameters at kwargs and inf args and kwargs.
    (
        implementation_13,
        {
            "c": _Type(int),
            "e": _Type(int),
        },
        (_Type(int), _Type(str), _Type(int)),
        True,
    ),
    # Set without args and kwargs and defaults.
    (
        implementation_13,
        {
            "c": _Type(int),
        },
        (_Type(int),),
        True,
    ),
    # Wrong.
    # Missed args with default, but inf args set.
    (
        implementation_13,
        {
            "c": _Type(int),
        },
        (_Type(int), _Type(int)),
        False,
    ),
    # Wrong inf args type.
    (
        implementation_13,
        {
            "c": _Type(int),
        },
        (_Type(int), _Type(str), _Type(str)),
        False,
    ),
    # Wrong inf kwargs type.
    (
        implementation_13,
        {
            "c": _Type(int),
            "n": _Type(list),
        },
        (_Type(int), _Type(str)),
        False,
    ),
)

if python_version_3_8:
    from .data_3_8 import *

    TEST_FUNCTION_IMPLEMENTATION_COMPARE = (
        *TEST_FUNCTION_IMPLEMENTATION_COMPARE,
        *TEST_FUNCTION_IMPLEMENTATION_COMPARE_FOR_3_8_PLUS,
    )
