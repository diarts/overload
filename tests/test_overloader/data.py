from overload.exception.overloader import (
    FunctionRegisterTypeError,
    MissedAnnotations,
    AnnotationCountError,
    ArgumentNameError,
    OverlappingError,
)


def default_func():
    def new_default_function(a: int, b: list):
        pass

    return new_default_function


def new_correct_func(a: str, b: int, c: tuple):
    pass


def func_with_and_without_annotations(a: str, b: int, d):
    pass


def func_without_annotation(a, b):
    pass


def func_with_less_args(a: str):
    pass


def func_with_mixed_args(b: str, a: int):
    pass


validation_of_register_func = (
    # Pytest parameters format:
    # default, strict, overlap, new_func, exception.
    # Correct validate.
    (default_func(), False, True, new_correct_func, None),
    (default_func(), False, True, default_func(), None),
    (default_func(), False, True, func_with_less_args, None),
    (default_func(), False, True, func_with_mixed_args, None),
    (default_func(), False, True, func_with_and_without_annotations, None),
    (default_func(), True, True, func_with_and_without_annotations, None),
    (default_func(), False, False, func_without_annotation, None),
    (default_func(), False, True, func_without_annotation, None),

    # Wrong parameters.
    (default_func(), False, True, int, FunctionRegisterTypeError),
    (default_func(), True, False, func_without_annotation,
     AnnotationCountError),
    (default_func(), True, True, func_without_annotation,
     AnnotationCountError),
    (default_func(), True, True, func_with_less_args, AnnotationCountError),
    (default_func(), True, True, func_with_mixed_args, ArgumentNameError),
    (default_func(), False, False, default_func(), OverlappingError),
)
