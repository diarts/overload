from overload.implementation.function import FunctionImplementation
from overload.type.type import _Type

_STRICT_TEST_FUNCTION_IMPLEMENTATION = FunctionImplementation(
    implementation=None,
    annotations={'test': _Type(int), 'test2': _Type(str)},
    overload=None,
    strict=True,
)

_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION = FunctionImplementation(
    implementation=None,
    annotations={'test': _Type(int), 'test2': _Type(str)},
    overload=None,
    strict=False,
)

TEST_FUNCTION_IMPLEMENTATION_COMPARE = (
    # Parameter format: implementation, named, unnamed, compare_result
    # Compare success.
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION, None, (_Type(int), _Type(str)),
     True),
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION, {'test': _Type(int)},
     (_Type(str),), True),
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION, {'test2': _Type(str)},
     (_Type(int),), True),
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION,
     {'test': _Type(int), 'test2': _Type(str), }, None, True),
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION,
     {'test2': _Type(str), 'test': _Type(int), }, None, True),
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION,
     {'test2': _Type(str), 'test': _Type(int), 'test3': _Type(list)}, None,
     True),
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION,
     {'test2': _Type(str), 'test': _Type(int), }, (_Type(list),), True),
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION, None,
     (_Type(int), _Type(str), _Type(list),), True),
    # Compare fail.
    # Unnamed parameter wrong sequence.
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION, None, (_Type(str), _Type(int),),
     False),
    # Unnamed parameter wrong value.
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION, None, (_Type(int), _Type(list),),
     False),
    # Named parameter wrong value.
    (_UNSTRICT_TEST_FUNCTION_IMPLEMENTATION, {'test': _Type(list)},
     (_Type(list),), False),
    # Strict implementation exceeded unnamed parameters count.
    (_STRICT_TEST_FUNCTION_IMPLEMENTATION, None,
     (_Type(int), _Type(str), _Type(list),), False),
    # Strict implementation exceeded named parameters count.
    (_STRICT_TEST_FUNCTION_IMPLEMENTATION,
     {'test2': _Type(str), 'test': _Type(int), 'test3': _Type(list)}, None,
     False),
    # Strict implementation exceeded named and unnamed parameters count.
    (_STRICT_TEST_FUNCTION_IMPLEMENTATION,
     {'test2': _Type(str), 'test': _Type(int), }, (_Type(list),), False),
)
