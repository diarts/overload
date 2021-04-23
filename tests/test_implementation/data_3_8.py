"""Functions for python >= 3.8 versions."""
from overload.implementation.function import FunctionImplementation
from overload.type.type import Args, Kwargs, _Type, _TypeHandler

TypeHandler = _TypeHandler()


# Function with one only args parameter.
def function_14(a: int, /):
    pass


implementation_14 = FunctionImplementation(
    function_14,
    TypeHandler.converting_annotations(function_14.__annotations__)
)


# Function with 2 only args parameters, one with default.
def function_15(a: int, b: str = 'test', /):
    pass


implementation_15 = FunctionImplementation(
    function_15,
    TypeHandler.converting_annotations(function_15.__annotations__)
)


# Function with 2 only args parameters, one with default and one args parameter
# with default.
def function_16(a: int, b: str = 'test', /, c: str = 'test'):
    pass


implementation_16 = FunctionImplementation(
    function_16,
    TypeHandler.converting_annotations(function_16.__annotations__)
)


# Function with all variance of parameter types.
def function_17(n: int, /,
                a: int, m: str = 'test', *args: Args[int],
                c: int, d: str = 'test', **kwargs: Kwargs[int]):
    pass


implementation_17 = FunctionImplementation(
    function_17,
    TypeHandler.converting_annotations(function_17.__annotations__)
)

TEST_FUNCTION_IMPLEMENTATION_COMPARE_FOR_3_8_PLUS = (
    # Parameter format: implementation, named, unnamed, compare_result
    # Function 14 - with one only args parameter.
    # Correct.
    # Set only args parameter in args.
    (implementation_14, {}, (_Type(int),), True),
    # Wrong.
    # Set only args parameter in kwargs.
    (implementation_14, {'a': _Type(int), }, (), False),
    # Parameter wrong type.
    (implementation_14, {}, (_Type(str),), False),

    # Function 15 - with 2 only args parameters, one with default.
    # Correct.
    # Set all parameters.
    (implementation_15, {}, (_Type(int), _Type(str)), True),
    # Set without default parameters.
    (implementation_15, {}, (_Type(int),), True),
    # Wrong.
    # Set all parameters in kwargs.
    (implementation_15, {'a': _Type(int), 'b': _Type(str)}, (), False),
    # Wrong default parameter type.
    (implementation_15, {}, (_Type(int), _Type(int)), False),

    # Function 16 - with 2 only args parameters, one with default and one args
    # parameter with default.
    # Correct.
    # Set all parameters in args.
    (implementation_16, {}, (_Type(int), _Type(str), _Type(str)), True),
    # Set only args parameters in args and simple args parameter in kwargs.
    (implementation_16, {'c': _Type(str)}, (_Type(int), _Type(str)), True),
    # Wrong.
    # Set only args parameters in args and kwargs and
    # simple args parameter in args.
    (implementation_16, {'b': _Type(str)}, (_Type(int), _Type(str)), False),

    # Function 17 - with all variance of parameter types.
    # Correct.
    # Set all parameters.
    (
        implementation_17,
        {
            "c": _Type(int),
            "d": _Type(str),
            "e": _Type(int),
        },
        (_Type(int), _Type(int), _Type(str), _Type(int)),
        True,
    ),
    # Set all without default kwargs.
    (
        implementation_17,
        {
            "c": _Type(int),
            "e": _Type(int),
        },
        (_Type(int), _Type(int), _Type(str), _Type(int)),
        True,
    ),
    # Wrong.
    # Mixed args parameters.
    (
        implementation_17,
        {
            "c": _Type(int),
            "e": _Type(int),
        },
        (_Type(int), _Type(str), _Type(int), _Type(int)),
        False,
    ),

)
