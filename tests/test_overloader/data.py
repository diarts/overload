from overload.exception.overloader import (
    FunctionRegisterTypeError,
    MissedAnnotations,
    AnnotationCountError,
    ArgumentNameError,
    OverlappingError,
)


def default_function(a: int, b: list):
    pass


def default_without_parameters():
    pass


def without_annotations(a, b):
    pass


def two_parameters_each_different_types(a: str, b: int):
    pass


def two_parameters_one_different_types(a: int, b: str):
    pass


def two_parameters_same_types(a: int, b: list):
    pass


def without_parameters():
    pass


def one_parameter_same_type(a: int):
    pass


def one_parameter_different_type(a: list):
    pass


def three_parameters_two_same_types(a: int, b: list, c: str):
    pass


def three_parameters_two_different_types(a: str, b: int, c: int):
    pass


def two_parameters_same_types_mixed(b: list, a: int):
    pass


def two_parameters_different_types_mixed(b: int, a: str):
    pass


FUNCTION_OVERLOADER_REGISTER = (
    # Pytest parameters format:
    # default, strict, overlap, new_func, exception.

    # Not function.
    (  # 1
        default_function,
        True,
        True,
        None,
        FunctionRegisterTypeError,
    ),

    # Missed annotations.
    (  # 2
        default_function,
        True,
        True,
        without_annotations,
        MissedAnnotations,
    ),

    # Function with equal count of parameters and each has different type.
    (  # 3
        default_function,
        True,
        True,
        two_parameters_each_different_types,
        None,
    ),
    (  # 4
        default_function,
        True,
        False,
        two_parameters_each_different_types,
        None,
    ),
    (  # 5
        default_function,
        False,
        True,
        two_parameters_each_different_types,
        None,
    ),
    (  # 6
        default_function,
        False,
        False,
        two_parameters_each_different_types,
        None,
    ),

    # Function with equal count of parameters, one has different type.
    (  # 7
        default_function,
        True,
        True,
        two_parameters_one_different_types,
        None,
    ),
    (  # 8
        default_function,
        False,
        True,
        two_parameters_one_different_types,
        None,
    ),
    (  # 9
        default_function,
        True,
        False,
        two_parameters_one_different_types,
        None,
    ),
    (  # 10
        default_function,
        False,
        False,
        two_parameters_one_different_types,
        None,
    ),

    # Function with equal count parameters, all parameters has same types.
    (  # 11
        default_function,  # default
        True,  # strict
        True,  # overlap
        two_parameters_same_types,  # new_func
        None,  # exception
    ),
    (  # 12
        default_function,  # default
        True,  # strict
        False,  # overlap
        two_parameters_same_types,  # new_func
        OverlappingError,  # exception
    ),
    (  # 13
        default_function,  # default
        False,  # strict
        True,  # overlap
        two_parameters_same_types,  # new_func
        None,  # exception
    ),
    (  # 14
        default_function,  # default
        False,  # strict
        False,  # overlap
        two_parameters_same_types,  # new_func
        OverlappingError,  # exception
    ),

    # Function without parameters.
    (  # 15
        default_function,  # default
        True,  # strict
        True,  # overlap
        without_parameters,  # new_func
        AnnotationCountError,  # exception
    ),
    (  # 16
        default_function,  # default
        False,  # strict
        True,  # overlap
        without_parameters,  # new_func
        None,  # exception
    ),
    (  # 17
        default_function,  # default
        False,  # strict
        False,  # overlap
        without_parameters,  # new_func
        None,  # exception
    ),

    # Default without parameters and new without parameters too.
    (  # 18
        default_without_parameters,  # default
        True,  # strict
        True,  # overlap
        without_parameters,  # new_func
        None,  # exception
    ),
    (  # 19
        default_without_parameters,  # default
        True,  # strict
        False,  # overlap
        without_parameters,  # new_func
        OverlappingError,  # exception
    ),

    # Function with one parameter same type.
    (  # 20
        default_function,  # default
        True,  # strict
        True,  # overlap
        one_parameter_same_type,  # new_func
        AnnotationCountError,  # exception
    ),
    (  # 21
        default_function,  # default
        False,  # strict
        True,  # overlap
        one_parameter_same_type,  # new_func
        None,  # exception
    ),
    (  # 22
        default_function,  # default
        False,  # strict
        False,  # overlap
        one_parameter_same_type,  # new_func
        None,  # exception
    ),

    # Function with one parameter different type.
    (  # 23
        default_function,  # default
        True,  # strict
        True,  # overlap
        one_parameter_different_type,  # new_func
        AnnotationCountError,  # exception
    ),
    (  # 24
        default_function,  # default
        False,  # strict
        True,  # overlap
        one_parameter_different_type,  # new_func
        None,  # exception
    ),
    (  # 25
        default_function,  # default
        False,  # strict
        False,  # overlap
        one_parameter_different_type,  # new_func
        None,  # exception
    ),

    # Function with three parameters, two has same type.
    (  # 26
        default_function,  # default
        True,  # strict
        True,  # overlap
        three_parameters_two_same_types,  # new_func
        AnnotationCountError,  # exception
    ),
    (  # 27
        default_function,  # default
        False,  # strict
        True,  # overlap
        three_parameters_two_same_types,  # new_func
        None,  # exception
    ),
    (  # 28
        default_function,  # default
        False,  # strict
        False,  # overlap
        three_parameters_two_same_types,  # new_func
        None,  # exception
    ),

    # Function with three parameters, two has different type.
    (  # 29
        default_function,  # default
        True,  # strict
        True,  # overlap
        three_parameters_two_different_types,  # new_func
        AnnotationCountError,  # exception
    ),
    (  # 30
        default_function,  # default
        False,  # strict
        True,  # overlap
        three_parameters_two_different_types,  # new_func
        None,  # exception
    ),
    (  # 31
        default_function,  # default
        False,  # strict
        False,  # overlap
        three_parameters_two_different_types,  # new_func
        None,  # exception
    ),

    # Function with two same parameters mixed.
    (  # 32
        default_function,  # default
        True,  # strict
        True,  # overlap
        two_parameters_same_types_mixed,  # new_func
        ArgumentNameError,  # exception
    ),
    (  # 33
        default_function,  # default
        False,  # strict
        True,  # overlap
        two_parameters_same_types_mixed,  # new_func
        None,  # exception
    ),
    (  # 34
        default_function,  # default
        True,  # strict
        False,  # overlap
        two_parameters_same_types_mixed,  # new_func
        ArgumentNameError,  # exception
    ),
    (  # 35
        default_function,  # default
        False,  # strict
        False,  # overlap
        two_parameters_same_types_mixed,  # new_func
        OverlappingError,  # exception
    ),

    # Function with two different parameters mixed.
    (  # 36
        default_function,  # default
        True,  # strict
        True,  # overlap
        two_parameters_different_types_mixed,  # new_func
        ArgumentNameError,  # exception
    ),
    (  # 37
        default_function,  # default
        False,  # strict
        True,  # overlap
        two_parameters_different_types_mixed,  # new_func
        None,  # exception
    ),
    (  # 38
        default_function,  # default
        True,  # strict
        False,  # overlap
        two_parameters_different_types_mixed,  # new_func
        ArgumentNameError,  # exception
    ),
    (  # 39
        default_function,  # default
        False,  # strict
        False,  # overlap
        two_parameters_different_types_mixed,  # new_func
        None,  # exception
    ),
)
