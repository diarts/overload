import pytest

from .data import TEST_FUNCTION_IMPLEMENTATION_COMPARE


@pytest.mark.implementation
@pytest.mark.parametrize(
    'implementation,named,unnamed,compare_result',
    TEST_FUNCTION_IMPLEMENTATION_COMPARE,
)
def test_function_implementation_compare(implementation, named, unnamed,
                                         compare_result):
    assert compare_result == implementation.compare(named, unnamed)
