from overload.exception.overloader import (
    FunctionRegisterTypeError,
    MissedAnnotations,
    AnnotationCountError,
    ArgumentNameError,
)


def default_func(a: int, b: list):
    pass


def func_without_annotation(a, b):
    pass


def func_with_less_args(a: str):
    pass


def func_with_mixed_args(b: str, a: int):
    pass


validation_of_register_func = (
    #  default, strict, new_func, exception
    (default_func, False, int, FunctionRegisterTypeError),
    (default_func, False, func_without_annotation, MissedAnnotations),
    (default_func, True, func_with_less_args, AnnotationCountError),
    (default_func, True, func_with_mixed_args, ArgumentNameError),
)
