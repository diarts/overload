from overload.type.type import _Type
from overload.exception.matrix import (
    ImplementationAlreadyRegistered,
)


def add_implementation_obj_1():
    pass


def add_implementation_obj_2():
    pass


def add_implementation_obj_3():
    pass


add_implementations = [
    # format: callable_, args, exception, row_count, column_count
    (add_implementation_obj_1, {'1': _Type(int)}, None,
     {'1': [_Type(int)]}, 1),
    (add_implementation_obj_1, None, ImplementationAlreadyRegistered, None,
     None),
    (add_implementation_obj_2, {'2': _Type(str)}, None,
     {'1': [_Type(int), None], '2': [None, _Type(str)]}, 2),
    (add_implementation_obj_3, {'1': _Type(str)}, None,
     {'1': [_Type(int), None, _Type(str)], '2': [None, _Type(str), None]}, 3),
]
