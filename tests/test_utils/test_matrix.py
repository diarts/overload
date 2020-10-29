import pytest

from overload.utils.matrix import _OverloadMatrix

from .data import add_implementations

add_implementation_matrix = _OverloadMatrix()


@pytest.mark.matrix
@pytest.mark.parametrize(
    'callable_,args,exception,rows,column_count',
    add_implementations,
)
def test_add_implementations(callable_, args, exception, rows,
                             column_count):
    if exception:
        with pytest.raises(exception):
            add_implementation_matrix[callable_] = args

    else:
        add_implementation_matrix[callable_] = args
        assert len(add_implementation_matrix.columns) == column_count
        assert add_implementation_matrix.rows == rows
